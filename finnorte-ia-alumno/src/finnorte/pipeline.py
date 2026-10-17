"""Flujos encadenados (T4): la salida de cada etapa es la entrada de la siguiente.

    flujo = Pipeline([
        Etapa("analizar",  prompt="analizar_requisito"),
        Etapa("casos",     prompt="generar_casos", usa=["analizar"]),
        Etapa("revisar",   prompt="revisar_casos", usa=["analizar", "casos"]),
    ])
    res = flujo.ejecutar({"requisito": "El sistema deberá…"})
    res.salidas["casos"], res.ok, res.bitacora

Cada etapa: renderiza su prompt con la entrada y las salidas previas → llama al modelo →
valida la salida contra el esquema JSON → si no es válida, reintenta con el error (control, T5).
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

import jsonschema

from . import llm, prompts, trazas


@dataclass
class Etapa:
    nombre: str
    prompt: str                      # id del prompt en prompts/
    version: int | None = None       # None = la más reciente
    usa: list[str] = field(default_factory=list)   # salidas previas que necesita
    validar: Callable[[Any, dict], list[str]] | None = None   # validación extra (reglas de negocio)
    reintentos: int = 1
    temperatura: float = 0.2


@dataclass
class ResultadoEtapa:
    nombre: str
    prompt: str
    ok: bool
    salida: Any
    errores: list[str]
    intentos: int
    latencia_ms: float
    costo_usd: float


@dataclass
class ResultadoFlujo:
    entrada: dict
    salidas: dict
    etapas: list[ResultadoEtapa]

    @property
    def ok(self) -> bool:
        return all(e.ok for e in self.etapas)

    @property
    def costo_usd(self) -> float:
        return sum(e.costo_usd for e in self.etapas)

    @property
    def latencia_ms(self) -> float:
        return sum(e.latencia_ms for e in self.etapas)

    def bitacora(self) -> list[dict]:
        return [e.__dict__ for e in self.etapas]


def validar_esquema(datos: Any, esquema: dict | None) -> list[str]:
    """Lista de errores de esquema (vacía si es válido)."""
    if esquema is None:
        return []
    if datos is None:
        return ["La salida no es JSON válido"]
    v = jsonschema.Draft202012Validator(esquema)
    return [f"{'/'.join(map(str, e.path)) or '(raíz)'}: {e.message}" for e in v.iter_errors(datos)]


class Pipeline:
    def __init__(self, etapas: list[Etapa], nombre: str = "flujo"):
        self.etapas = etapas
        self.nombre = nombre

    def ejecutar(self, entrada: dict, detener_en_error: bool = True) -> ResultadoFlujo:
        salidas: dict = {}
        resultados: list[ResultadoEtapa] = []
        for etapa in self.etapas:
            # TODO(A2): implementa esta parte (ver docstring y pruebas)
            raise NotImplementedError("Pendiente: A2")
            resultados.append(res)
            salidas[etapa.nombre] = res.salida
            trazas.registrar("etapa", flujo=self.nombre, etapa=res.nombre, prompt=res.prompt, ok=res.ok,
                             errores=res.errores, intentos=res.intentos, latencia_ms=res.latencia_ms,
                             costo_usd=round(res.costo_usd, 6))
            if not res.ok and detener_en_error:
                break
        return ResultadoFlujo(entrada, salidas, resultados)
