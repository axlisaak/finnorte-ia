"""Controles contra errores del modelo (T5, T6, T11).

Cada control es una función pura y probable con pytest. Combínalos en tu flujo:
- verificar_citas: toda fuente citada debe existir entre los fragmentos recuperados.
- debe_abstenerse: si la recuperación no alcanza el umbral, no se llama al modelo.
- autocritica: una segunda llamada revisa la respuesta contra el contexto (cuesta otra llamada).
- filtrar_clasificacion: nunca pasar documentos confidenciales al prompt.
- sanear_salida: quita enlaces/imágenes externas y PII antes de mostrar (T11).
"""
from __future__ import annotations

import re
from typing import Iterable

from . import llm, pii
from .retrieval import Resultado

RESPUESTA_ABSTENCION = "No encuentro esa información en la documentación disponible. Te sugiero consultarlo con el área responsable."


def verificar_citas(fuentes_citadas: Iterable[str], recuperados: list[Resultado]) -> list[str]:
    """Errores por citas inventadas o ausentes. Acepta 'doc#n' o solo 'doc'."""
    # TODO(AV1): implementa esta parte (ver docstring y pruebas)
    raise NotImplementedError("Pendiente: AV1")


def debe_abstenerse(recuperados: list[Resultado], umbral: float) -> bool:
    """True si no hay contexto suficiente para responder."""
    # TODO(AV1): implementa esta parte (ver docstring y pruebas)
    raise NotImplementedError("Pendiente: AV1")


def filtrar_clasificacion(recuperados: list[Resultado], permitidas=("publica", "interna")) -> list[Resultado]:
    # TODO(AV2): implementa esta parte (ver docstring y pruebas)
    raise NotImplementedError("Pendiente: AV2")


def sanear_salida(texto: str, dominios_permitidos=("finnorte.mx",)) -> tuple[str, list[str]]:
    """Quita imágenes/enlaces a dominios ajenos y enmascara PII. Devuelve (texto, avisos)."""
    # TODO(AV2): implementa esta parte (ver docstring y pruebas)
    raise NotImplementedError("Pendiente: AV2")


def autocritica(respuesta: str, contexto: str, pregunta: str) -> dict:
    """Pide al modelo que verifique su propia respuesta contra el contexto. Devuelve
    {"soportada": bool, "problemas": [...]}; si el JSON falla, asume no soportada."""
    sistema = ("Eres un verificador estricto. Solo juzgas si cada afirmación de la RESPUESTA está respaldada "
               "por el CONTEXTO. No uses conocimiento externo.")
    usuario = (f"CONTEXTO:\n{contexto}\n\nPREGUNTA: {pregunta}\n\nRESPUESTA:\n{respuesta}\n\n"
               'Devuelve JSON: {"soportada": true|false, "problemas": ["afirmación sin respaldo", ...]}')
    r = llm.generar(usuario, sistema, json=True, temperatura=0.0, etiqueta="control/autocritica")
    d = r.datos if isinstance(r.datos, dict) else {}
    return {"soportada": bool(d.get("soportada", False)), "problemas": list(d.get("problemas", []))}
