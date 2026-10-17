"""Línea de comandos:  python -m finnorte <comando>

  info                                  proveedor, modelo y embeddings configurados
  probar                                una llamada mínima al modelo (verifica tu llave)
  buscar "consulta" [--palabras] [--k 4] [--corpus corpus/comun]
  preguntar "pregunta" [--sin-rag] [--sin-controles] [--v 2]
  evaluar evals/comun.jsonl [--rep 3] [--contrato contrato_calidad.yaml] [--salida bitacora/eval.json]
          [--sistema finnorte.variante:sistema]   evalúa TU sistema (función entrada->dict) en lugar del caso guía
                                        termina con código 1 si no se cumple el contrato (para CI)
  trazas                                resumen de la bitácora (llamadas, tokens, costo, latencia)
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys

from . import evaluacion, llm, trazas
from .config import RAIZ, config


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="finnorte")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    sub.add_parser("probar")
    b = sub.add_parser("buscar"); b.add_argument("consulta"); b.add_argument("--palabras", action="store_true")
    b.add_argument("--k", type=int, default=4); b.add_argument("--corpus", default=str(RAIZ / "corpus" / "comun"))
    p = sub.add_parser("preguntar"); p.add_argument("pregunta"); p.add_argument("--sin-rag", action="store_true")
    p.add_argument("--sin-controles", action="store_true"); p.add_argument("--v", type=int)
    p.add_argument("--corpus", default=str(RAIZ / "corpus" / "comun"))
    e = sub.add_parser("evaluar"); e.add_argument("casos"); e.add_argument("--rep", type=int, default=1)
    e.add_argument("--contrato"); e.add_argument("--salida"); e.add_argument("--sin-rag", action="store_true")
    e.add_argument("--sin-controles", action="store_true"); e.add_argument("--v", type=int)
    e.add_argument("--corpus", default=str(RAIZ / "corpus" / "comun"))
    e.add_argument("--sistema", help="modulo:funcion de tu sistema, p. ej. finnorte.variante:sistema")
    sub.add_parser("trazas")
    a = ap.parse_args(argv)

    if a.cmd == "info":
        c = config()
        print(f"LLM: {c.llm_proveedor} / {c.llm_modelo}\nEmbeddings: {c.emb_proveedor} / {c.emb_modelo}")
        return 0
    if a.cmd == "probar":
        r = llm.generar('Responde solo con JSON: {"ok": true, "saludo": "hola FinNorte"}', json=True, etiqueta="probar")
        print(r.texto, f"\n→ {r.proveedor}/{r.modelo} · {r.tokens_entrada}+{r.tokens_salida} tokens · {r.latencia_ms} ms · US${r.costo_usd:.6f}")
        return 0
    if a.cmd == "buscar":
        from .retrieval import Indice
        ind = Indice.desde_carpeta(a.corpus)
        res = ind.buscar_palabras(a.consulta, a.k) if a.palabras else ind.buscar(a.consulta, a.k)
        for r in res:
            print(f"{r.puntaje:7.3f}  {r.fragmento.id:22s} {r.fragmento.titulo}")
        return 0
    if a.cmd == "evaluar" and a.sistema:
        import importlib
        mod, fn = a.sistema.split(":")
        sistema = getattr(importlib.import_module(mod), fn)
        return _evaluar(sistema, a)
    if a.cmd in ("preguntar", "evaluar"):
        from .asistente import Asistente
        asis = Asistente.crear(a.corpus, usar_rag=not a.sin_rag, controles=not a.sin_controles, version_prompt=a.v)
        if a.cmd == "preguntar":
            print(json.dumps(asis.responder(a.pregunta), ensure_ascii=False, indent=2))
            return 0
        return _evaluar(asis.responder, a)
    if a.cmd == "trazas":
        ev = trazas.leer("llm")
        ok = [x for x in ev if x.get("ok")]
        if not ev:
            print("Bitácora vacía.")
            return 0
        lat = sorted(x["latencia_ms"] for x in ok) or [0]
        print(f"Llamadas: {len(ev)} (fallidas: {len(ev) - len(ok)})")
        print(f"Tokens: {sum(x.get('tokens_entrada', 0) for x in ok)} entrada · {sum(x.get('tokens_salida', 0) for x in ok)} salida")
        print(f"Costo: US${sum(x.get('costo_usd', 0) for x in ok):.4f}")
        print(f"Latencia: mediana {statistics.median(lat):.0f} ms · p95 {lat[int(0.95 * (len(lat) - 1))]:.0f} ms")
        return 0
    return 2


def _evaluar(sistema, a) -> int:
    res = evaluacion.evaluar(sistema, evaluacion.cargar_casos(a.casos), repeticiones=a.rep, etiqueta=a.casos)
    print(json.dumps(res["metricas"], ensure_ascii=False, indent=2))
    if a.salida:
        evaluacion.guardar_reporte(res, a.salida)
    if a.contrato:
        filas = evaluacion.revisar_contrato(res["metricas"], evaluacion.cargar_contrato(a.contrato))
        print("\n" + evaluacion.tabla_markdown(filas))
        if not all(f["cumple"] for f in filas):
            print("\n✗ El contrato de calidad NO se cumple.")
            return 1
        print("\n✓ Contrato de calidad cumplido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
