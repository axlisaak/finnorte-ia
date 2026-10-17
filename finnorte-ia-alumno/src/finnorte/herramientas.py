"""Agente con herramientas (T10): el modelo PROPONE una acción en JSON; tu código decide y la ejecuta.

Funciona igual con cualquier proveedor porque no depende del "function calling" nativo:
el modelo responde
  {"accion": "usar", "herramienta": "nombre", "argumentos": {...}, "razon": "..."}
o
  {"accion": "responder", "respuesta": "...", "fuentes": [...]}

Reglas que el código hace cumplir (no el modelo):
- Solo herramientas registradas; argumentos validados contra su esquema.
- Herramientas marcadas `sensible=True` requieren confirmación humana.
- Máximo de pasos para evitar bucles; todo queda en la bitácora.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

import jsonschema

from . import llm, trazas


@dataclass
class Herramienta:
    nombre: str
    descripcion: str
    esquema: dict                      # JSON Schema de los argumentos
    funcion: Callable[..., Any]
    sensible: bool = False             # requiere confirmación humana


@dataclass
class Paso:
    n: int
    propuesta: dict
    resultado: Any = None
    estado: str = ""                   # ejecutada | rechazada | invalida | respuesta | sin_confirmar


@dataclass
class ResultadoAgente:
    respuesta: str
    fuentes: list
    pasos: list[Paso] = field(default_factory=list)
    terminado: bool = True


def _catalogo(herrs: dict[str, Herramienta]) -> str:
    return "\n".join(f"- {h.nombre}: {h.descripcion}. Argumentos (JSON Schema): {json.dumps(h.esquema, ensure_ascii=False)}"
                     + (" [SENSIBLE: requiere confirmación]" if h.sensible else "") for h in herrs.values())


SISTEMA_AGENTE = """Eres un asistente de ingeniería de FinNorte que resuelve tareas en pasos.
En cada turno devuelve SOLO un JSON con una de dos formas:
{{"accion": "usar", "herramienta": "<nombre>", "argumentos": {{...}}, "razon": "<por qué>"}}
{{"accion": "responder", "respuesta": "<respuesta final>", "fuentes": ["<id>", ...]}}
Herramientas disponibles:
{catalogo}
No inventes herramientas ni resultados. Si una herramienta falla, decide si reintentar o responder con lo que tienes."""


def ejecutar_agente(tarea: str, herramientas: list[Herramienta], confirmar: Callable[[Herramienta, dict], bool] | None = None,
                    max_pasos: int = 5, contexto: str = "") -> ResultadoAgente:
    herrs = {h.nombre: h for h in herramientas}
    sistema = SISTEMA_AGENTE.format(catalogo=_catalogo(herrs))
    historial: list[dict] = []
    pasos: list[Paso] = []
    mensaje = f"Tarea: {tarea}" + (f"\n\nContexto:\n{contexto}" if contexto else "")
    # TODO(A4): implementa esta parte (ver docstring y pruebas)
    raise NotImplementedError("Pendiente: A4")
