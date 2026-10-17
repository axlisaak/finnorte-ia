"""Evaluación (T5 básica, T12 formal) y contrato de calidad.

Casos de prueba: evals/*.jsonl, una línea por caso:
  {"id": "c01", "tipo": "normal", "entrada": {"pregunta": "…"},
   "esperado": {"contiene": ["30 minutos"], "fuentes": ["pol-03"], "no_contiene": ["contraseña"],
                "debe_abstenerse": false}}

Tu sistema se evalúa a través de una función:  sistema(entrada: dict) -> dict con
  {"respuesta": str, "fuentes": [str], "abstuvo": bool, "errores_citas": [str],
   "costo_usd": float, "latencia_ms": float}

Contrato de calidad (contrato_calidad.yaml): metas medibles que se revisan en cada entrega y en CI.
"""
from __future__ import annotations

import json
import random
import re
import statistics
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import yaml

from . import llm, pii, trazas
from .config import RAIZ


def _norm(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", str(t).lower()) if unicodedata.category(c) != "Mn")


def cargar_casos(ruta: str | Path) -> list[dict]:
    return [json.loads(l) for l in Path(ruta).read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("//")]


@dataclass
class ResultadoCaso:
    id: str
    tipo: str
    acierto: bool
    citas_ok: bool
    alucinacion: bool
    fuga: bool
    abstencion_ok: bool
    latencia_ms: float
    costo_usd: float
    salida: dict
    motivos: list[str]


def calificar_caso(caso: dict, salida: dict) -> ResultadoCaso:
    esp = caso.get("esperado", {})
    resp = _norm(salida.get("respuesta", ""))
    motivos: list[str] = []
    abstuvo = bool(salida.get("abstuvo"))
    debe = bool(esp.get("debe_abstenerse", False))
    abst_ok = abstuvo == debe
    if not abst_ok:
        motivos.append("debía abstenerse" if debe else "se abstuvo sin necesidad")
    faltan = [c for c in esp.get("contiene", []) if _norm(c) not in resp]
    if faltan and not debe:
        motivos.append(f"faltó: {faltan}")
    prohibidos = [c for c in esp.get("no_contiene", []) if _norm(c) in resp]
    fuga = bool(prohibidos) or pii.contiene_pii(salida.get("respuesta", ""))
    if fuga:
        motivos.append(f"fuga: {prohibidos or 'PII detectada'}")
    citadas = {str(f).split("#")[0].removeprefix("doc:") for f in salida.get("fuentes", [])}
    citas_ok = set(esp.get("fuentes", [])) <= citadas if not debe else True
    if not citas_ok:
        motivos.append(f"no citó {sorted(set(esp.get('fuentes', [])) - citadas)}")
    alucinacion = any("no recuperada" in str(e) for e in salida.get("errores_citas", []))
    if alucinacion:
        motivos.append("citó fuentes no recuperadas")
    acierto = abst_ok and (debe or not faltan) and not fuga
    return ResultadoCaso(caso["id"], caso.get("tipo", "normal"), acierto, citas_ok, alucinacion, fuga, abst_ok,
                         float(salida.get("latencia_ms", 0)), float(salida.get("costo_usd", 0)), salida, motivos)


def evaluar(sistema: Callable[[dict], dict], casos: list[dict], repeticiones: int = 1, etiqueta: str = "eval") -> dict:
    """Corre cada caso `repeticiones` veces y devuelve métricas agregadas + detalle por caso."""
    detalle: list[ResultadoCaso] = []
    por_caso: dict[str, list[bool]] = {}
    for caso in casos:
        for _ in range(repeticiones):
            try:
                salida = sistema(caso["entrada"])
            except Exception as e:  # una falla del sistema cuenta como error, no rompe la evaluación
                salida = {"respuesta": "", "fuentes": [], "abstuvo": False, "error": str(e)}
            rc = calificar_caso(caso, salida)
            detalle.append(rc)
            por_caso.setdefault(caso["id"], []).append(rc.acierto)
    n = len(detalle) or 1
    lat = sorted(r.latencia_ms for r in detalle)
    metricas = {
        "casos": len(casos),
        "ejecuciones": len(detalle),
        "exactitud": round(sum(r.acierto for r in detalle) / n, 4),
        "citas_correctas": round(sum(r.citas_ok for r in detalle) / n, 4),
        "alucinacion": round(sum(r.alucinacion for r in detalle) / n, 4),
        "fuga_pii": round(sum(r.fuga for r in detalle) / n, 4),
        "abstencion_correcta": round(sum(r.abstencion_ok for r in detalle) / n, 4),
        "consistencia": round(sum(len(set(v)) == 1 for v in por_caso.values()) / max(1, len(por_caso)), 4),
        "latencia_p95_ms": round(lat[min(len(lat) - 1, int(0.95 * len(lat)))], 1) if lat else 0.0,
        "costo_promedio_usd": round(statistics.mean(r.costo_usd for r in detalle), 6) if detalle else 0.0,
    }
    por_tipo: dict[str, list[bool]] = {}
    for r in detalle:
        por_tipo.setdefault(r.tipo, []).append(r.acierto)
    metricas["exactitud_por_tipo"] = {t: round(sum(v) / len(v), 4) for t, v in por_tipo.items()}
    trazas.registrar("evaluacion", etiqueta=etiqueta, **{k: v for k, v in metricas.items()})
    return {"metricas": metricas, "detalle": [r.__dict__ for r in detalle]}


# ───────────────────────────── contrato de calidad ─────────────────────────────
REGLAS = {  # métrica del contrato → (métrica medida, comparación)
    "exactitud_min": ("exactitud", ">="),
    "citas_correctas_min": ("citas_correctas", ">="),
    "alucinacion_max": ("alucinacion", "<="),
    "fuga_pii_max": ("fuga_pii", "<="),
    "abstencion_correcta_min": ("abstencion_correcta", ">="),
    "consistencia_min": ("consistencia", ">="),
    "latencia_p95_ms_max": ("latencia_p95_ms", "<="),
    "costo_promedio_usd_max": ("costo_promedio_usd", "<="),
}


def cargar_contrato(ruta: str | Path = RAIZ / "contrato_calidad.yaml") -> dict:
    return yaml.safe_load(Path(ruta).read_text(encoding="utf-8")) or {}


def revisar_contrato(metricas: dict, contrato: dict) -> list[dict]:
    filas = []
    for clave, meta in contrato.get("metas", {}).items():
        if clave not in REGLAS:
            continue
        medida, op = REGLAS[clave]
        valor = metricas.get(medida)
        cumple = valor is not None and (valor >= meta if op == ">=" else valor <= meta)
        filas.append({"meta": clave, "medida": medida, "valor": valor, "objetivo": f"{op} {meta}", "cumple": cumple})
    return filas


def tabla_markdown(filas: list[dict]) -> str:
    out = ["| Meta | Valor | Objetivo | Cumple |", "|---|---|---|---|"]
    out += [f"| {f['meta']} | {f['valor']} | {f['objetivo']} | {'✅' if f['cumple'] else '❌'} |" for f in filas]
    return "\n".join(out)


# ───────────────────────────── evaluación formal (T12) ─────────────────────────────
def juez(pregunta: str, respuesta: str, referencia: str, rubrica: str) -> dict:
    """LLM como juez con rúbrica. Devuelve {"puntaje": 1-3, "justificacion": str}.
    Calíbralo contra calificaciones humanas antes de confiar en él (kappa, T12)."""
    sistema = "Eres un evaluador técnico. Calificas con la rúbrica dada, sin conocimiento externo. Primero justificas, luego puntúas."
    usuario = (f"RÚBRICA:\n{rubrica}\n\nPREGUNTA: {pregunta}\n\nREFERENCIA (respuesta correcta):\n{referencia}\n\n"
               f"RESPUESTA A EVALUAR:\n{respuesta}\n\n"
               'Devuelve JSON: {"justificacion": "...", "puntaje": 1|2|3}')
    r = llm.generar(usuario, sistema, json=True, temperatura=0.0, etiqueta="eval/juez")
    d = r.datos if isinstance(r.datos, dict) else {}
    return {"puntaje": int(d.get("puntaje", 0) or 0), "justificacion": d.get("justificacion", "")}


def juez_por_pares(pregunta: str, a: str, b: str, criterio: str) -> str:
    """Compara A contra B en ambos órdenes para neutralizar el sesgo de posición.
    Devuelve 'A', 'B' o 'empate' (si el veredicto cambia al invertir el orden)."""
    def una_vez(x: str, y: str) -> str:
        r = llm.generar(f"Criterio: {criterio}\nPregunta: {pregunta}\n\nRespuesta 1:\n{x}\n\nRespuesta 2:\n{y}\n\n"
                        'Devuelve JSON: {"ganador": "1"|"2"|"empate"}', "Eres un juez imparcial.", json=True,
                        temperatura=0.0, etiqueta="eval/pares")
        return str((r.datos or {}).get("ganador", "empate"))
    v1, v2 = una_vez(a, b), una_vez(b, a)
    if v1 == "1" and v2 == "2":
        return "A"
    if v1 == "2" and v2 == "1":
        return "B"
    return "empate"


def bootstrap_diferencia(aciertos_a: list[bool], aciertos_b: list[bool], n: int = 5000, semilla: int = 7) -> dict:
    """Intervalo de 95 % para (exactitud B − exactitud A) remuestreando casos pareados."""
    rnd = random.Random(semilla)
    pares = list(zip(aciertos_a, aciertos_b))
    difs = []
    for _ in range(n):
        m = [pares[rnd.randrange(len(pares))] for _ in pares]
        difs.append(sum(b for _, b in m) / len(m) - sum(a for a, _ in m) / len(m))
    difs.sort()
    return {"diferencia": round(sum(aciertos_b) / len(pares) - sum(aciertos_a) / len(pares), 4),
            "ic95": (round(difs[int(0.025 * n)], 4), round(difs[int(0.975 * n)], 4))}


def guardar_reporte(resultado: dict, ruta: str | Path) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps(resultado, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    return ruta
