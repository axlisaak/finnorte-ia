"""Guía S2 (viernes 23 oct) · Flujo de 4 etapas: solicitud de cambio → análisis → plan → checklist → nota.

    python guia/s2_flujo_cambios.py

Qué hace
  1. Corre el flujo con 3 solicitudes (una clara, una ambigua y una de riesgo bajo).
  2. Valida cada salida contra su esquema JSON (y reintenta si falla).
  3. Imprime la matriz de trazabilidad: solicitud → etapa → artefacto → validación.
  4. Repite la solicitud 1 tres veces para ver la consistencia del riesgo asignado.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from finnorte.pipeline import Etapa, Pipeline
from finnorte.retrieval import guardar_resultados


def checklist_cubre_reversa(salida, previas):
    """Regla de negocio (código, no modelo): riesgo alto ⇒ el checklist incluye la reversa."""
    if previas.get("analizar", {}).get("riesgo") == "alto":
        if not any(i.get("origen", "").startswith("plan.reversa") for i in salida.get("checklist", [])):
            return ["Riesgo alto sin punto de checklist para la reversa (plan.reversa)"]
    return []


FLUJO = Pipeline([
    Etapa("analizar", "cambio_analizar"),
    Etapa("plan", "cambio_plan", usa=["analizar"]),
    Etapa("checklist", "cambio_checklist", usa=["analizar", "plan"], validar=checklist_cubre_reversa),
    Etapa("nota", "cambio_nota", usa=["analizar", "plan"]),
], nombre="cambios")

SOLICITUDES = {
    "CHG-1": "Agregar validación de Idempotency-Key al endpoint POST /v1/transferencias de pagos-api para evitar cobros duplicados.",
    "CHG-2": "Mejorar el servicio de notificaciones.",
    "CHG-3": "Cambiar el texto del pie de página del portal de desarrolladores.",
}
matriz = []
for cid, sol in SOLICITUDES.items():
    res = FLUJO.ejecutar({"solicitud": sol})
    print(f"\n{cid}: {'OK' if res.ok else 'FALLÓ'} · US${res.costo_usd:.5f} · {res.latencia_ms:.0f} ms")
    for e in res.etapas:
        print(f"  {e.nombre:10s} {e.prompt:22s} intentos={e.intentos} {'✓' if e.ok else '✗ ' + '; '.join(e.errores[:2])}")
        matriz.append({"solicitud": cid, "etapa": e.nombre, "prompt": e.prompt, "valida": e.ok, "intentos": e.intentos})
    if res.ok:
        print("  riesgo:", res.salidas["analizar"]["riesgo"], "· preguntas abiertas:", res.salidas["analizar"]["preguntas_abiertas"])

riesgos = [FLUJO.ejecutar({"solicitud": SOLICITUDES["CHG-1"]}).salidas.get("analizar", {}).get("riesgo") for _ in range(3)]
print("\nConsistencia de CHG-1 en 3 ejecuciones:", riesgos)
print("Matriz guardada en", guardar_resultados("s2_trazabilidad", matriz))
