"""Guía S7 (viernes 27 nov) · Reporte de calidad y operación a partir de la bitácora.

    python guia/s7_reporte.py --eval bitacora/eval_final.json > REPORTE_CALIDAD.md

Junta: métricas contra el contrato, costo y latencia reales de la bitácora, versiones de prompt usadas
y los casos fallidos con su motivo. Es la base de la sección de calidad de la Entrega final.
"""
import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from finnorte import evaluacion, trazas

ap = argparse.ArgumentParser(); ap.add_argument("--eval", required=True); a = ap.parse_args()
r = json.loads(Path(a.eval).read_text(encoding="utf-8"))
m = r["metricas"]
filas = evaluacion.revisar_contrato(m, evaluacion.cargar_contrato())
llm_ev = [e for e in trazas.leer("llm") if e.get("ok")]
lat = sorted(e["latencia_ms"] for e in llm_ev) or [0]
print("# Reporte de calidad\n")
print(f"Casos: {m['casos']} · ejecuciones: {m['ejecuciones']}\n")
print("## Contrato de calidad\n" + evaluacion.tabla_markdown(filas) + "\n")
print("## Exactitud por tipo de caso\n| Tipo | Exactitud |\n|---|---|")
for t, v in m["exactitud_por_tipo"].items():
    print(f"| {t} | {v:.2f} |")
print("\n## Operación (bitácora)\n")
print(f"- Llamadas al modelo: {len(llm_ev)} · costo total US${sum(e.get('costo_usd', 0) for e in llm_ev):.4f}")
print(f"- Latencia por llamada: mediana {statistics.median(lat):.0f} ms · p95 {lat[int(0.95 * (len(lat) - 1))]:.0f} ms")
print(f"- Prompts usados: {dict(Counter(e.get('etiqueta', '').split('/')[-1] for e in llm_ev).most_common(8))}")
print("\n## Casos fallidos\n| Caso | Tipo | Motivo |\n|---|---|---|")
for d in r["detalle"]:
    if not d["acierto"]:
        print(f"| {d['id']} | {d['tipo']} | {'; '.join(d['motivos'])} |")
