"""TU SISTEMA: el motor de la variante de tu equipo.

Contrato mínimo (lo usa `python -m finnorte evaluar ... --sistema finnorte.variante:sistema`,
la API de la semana 4 y la interfaz de la semana 5):

    sistema(entrada: dict) -> dict con
        respuesta: str        el artefacto final en texto (casos, hallazgos, respuesta, README, triage)
        fuentes: list[str]    ids de fragmentos/documentos del corpus que respaldan la salida
        abstuvo: bool         True si la entrada está fuera de alcance o no hay contexto suficiente
        errores_citas: list   salida de controles.verificar_citas
        artefacto: dict       (opcional) la salida estructurada (JSON) de tu última etapa
        costo_usd, latencia_ms

Construye esto por incrementos:
  A1  → INDICE con el corpus de tu variante (corpus/<variante>/) y búsqueda semántica
  A2  → FLUJO de 4 etapas con prompts versionados en prompts/ y esquemas en prompts/esquemas/
  Av1 → RAG (contexto en el prompt) + controles + evaluación contra tu contrato de calidad
"""
from __future__ import annotations

import time
from pathlib import Path

from . import controles
from .config import RAIZ
from .pipeline import Etapa, Pipeline
from .retrieval import Indice, contexto_para_prompt

VARIANTE = "v5-triage"          # v1-qa | v2-revisor | v3-soporte | v4-documentador | v5-triage
_INDICE: Indice | None = None


def indice() -> Indice:
    global _INDICE
    if _INDICE is None:
        _INDICE = Indice.desde_carpeta(RAIZ / "corpus" / VARIANTE)
    return _INDICE


def leer_entrada(entrada: dict) -> str:
    """Normaliza la entrada de los casos de evaluación a texto."""
    if "archivo" in entrada:
        return (RAIZ / entrada["archivo"]).read_text(encoding="utf-8")
    for clave in ("requisito", "codigo", "pregunta", "log"):
        if clave in entrada:
            return str(entrada[clave])
    raise ValueError(f"Entrada sin campo reconocido: {list(entrada)}")


# TODO(A2): define tus etapas. Ejemplo para v1-qa:
#   Etapa("analizar", "qa_analizar"), Etapa("casos", "qa_casos", usa=["analizar"]),
#   Etapa("revisar", "qa_revisar", usa=["analizar", "casos"]), Etapa("pytest", "qa_pytest", usa=["casos"])
FLUJO = Pipeline([], nombre=VARIANTE)


def sistema(entrada: dict) -> dict:
    t0 = time.perf_counter()
    texto = leer_entrada(entrada)
    # TODO(Avance 1): recupera contexto → abstención → ejecuta el FLUJO con {"entrada": texto, "contexto": ...}
    #                 → verifica citas → sanea la salida → arma el dict de salida.
    raise NotImplementedError("Implementa tu sistema (ver docstring y el caso guía en asistente.py)")
