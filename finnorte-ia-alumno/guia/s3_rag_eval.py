"""Guía S3 (viernes 30 oct) · ¿Cuánto aportan el contexto y los controles? Medido, no opinado.

    python guia/s3_rag_eval.py [--rep 2]

Corre evals/comun.jsonl en 4 configuraciones y compara contra el contrato de calidad:
  A  prompt v1, sin RAG, sin controles        (línea base ingenua)
  B  prompt v2, sin RAG                        (solo mejor prompt)
  C  prompt v2, con RAG, sin controles
  D  prompt v2, con RAG y controles            (el motor del Avance 1)
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from finnorte import evaluacion
from finnorte.asistente import Asistente

ap = argparse.ArgumentParser(); ap.add_argument("--rep", type=int, default=1); a = ap.parse_args()
casos = evaluacion.cargar_casos("evals/comun.jsonl")
contrato = evaluacion.cargar_contrato()
CONFIGS = {
    "A v1 sin RAG": dict(version_prompt=1, usar_rag=False, controles=False),
    "B v2 sin RAG": dict(version_prompt=2, usar_rag=False, controles=False),
    "C v2 + RAG": dict(version_prompt=2, usar_rag=True, controles=False),
    "D v2 + RAG + controles": dict(version_prompt=2, usar_rag=True, controles=True),
}
tabla, aciertos = [], {}
for nombre, op in CONFIGS.items():
    asis = Asistente.crear(**op)
    r = evaluacion.evaluar(asis.responder, casos, repeticiones=a.rep, etiqueta=nombre)
    m = r["metricas"]
    aciertos[nombre] = [d["acierto"] for d in r["detalle"]]
    cumple = all(f["cumple"] for f in evaluacion.revisar_contrato(m, contrato))
    tabla.append((nombre, m["exactitud"], m["alucinacion"], m["fuga_pii"], m["abstencion_correcta"], m["latencia_p95_ms"], m["costo_promedio_usd"], cumple))
    evaluacion.guardar_reporte(r, f"bitacora/s3_{nombre.split()[0]}.json")
print("\n| Config | Exactitud | Alucinación | Fuga | Abstención ok | p95 ms | US$/resp | Contrato |")
print("|---|---|---|---|---|---|---|---|")
for f in tabla:
    print(f"| {f[0]} | {f[1]:.2f} | {f[2]:.2f} | {f[3]:.2f} | {f[4]:.2f} | {f[5]:.0f} | {f[6]:.5f} | {'✅' if f[7] else '❌'} |")
ic = evaluacion.bootstrap_diferencia(aciertos["A v1 sin RAG"], aciertos["D v2 + RAG + controles"])
print(f"\nD − A en exactitud: {ic['diferencia']:+.2f} (IC 95 % {ic['ic95']}). Si el intervalo incluye 0, aún no puedes afirmar mejora.")
