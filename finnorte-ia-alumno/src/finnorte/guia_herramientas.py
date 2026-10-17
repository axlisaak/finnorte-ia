"""Herramientas del caso guía (S5): el modelo puede proponerlas; el código las valida y ejecuta.

- buscar_manual(consulta)                 → fragmentos del Manual de Ingeniería (RAG)
- revisar_ventana_despliegue(fecha, riesgo) → regla determinista de ing-03 (no la decide el modelo)
- crear_ticket_cambio(titulo, riesgo)      → SENSIBLE: crea un ticket (simulado); requiere confirmación
"""
from __future__ import annotations

import datetime as dt
import itertools

from .herramientas import Herramienta
from .retrieval import Indice

_folios = itertools.count(1042)
TICKETS: list[dict] = []


def herramientas_guia(indice: Indice) -> list[Herramienta]:
    def buscar_manual(consulta: str, k: int = 3):
        return [{"id": r.fragmento.id, "titulo": r.fragmento.titulo, "texto": r.fragmento.texto[:600]}
                for r in indice.buscar(consulta, k=k) if r.fragmento.clasificacion != "confidencial"]

    def revisar_ventana_despliegue(fecha: str, riesgo: str):
        d = dt.date.fromisoformat(fecha)
        if (d.month == 12 and d.day >= 15) or (d.month == 1 and d.day <= 6):
            return {"permitido": False, "motivo": "Congelamiento de fin de año (15 dic – 6 ene)", "fuente": "ing-03"}
        if d.day in (14, 15, 29, 30, 31):
            return {"permitido": False, "motivo": "Congelamiento por pago de nómina (días 14, 15, 29, 30 y 31)", "fuente": "ing-03"}
        if riesgo == "alto":
            ok = d.weekday() in (1, 3)
            return {"permitido": ok, "motivo": "Riesgo alto: martes o jueves 22:00–02:00" + ("" if ok else "; esa fecha no es martes ni jueves"), "fuente": "ing-03"}
        ok = d.weekday() <= 3
        return {"permitido": ok, "motivo": "Riesgo medio/bajo: lunes a jueves 10:00–17:00" + ("" if ok else "; esa fecha es viernes o fin de semana"), "fuente": "ing-03"}

    def crear_ticket_cambio(titulo: str, riesgo: str, fecha: str):
        t = {"folio": f"CHG-{next(_folios)}", "titulo": titulo, "riesgo": riesgo, "fecha": fecha, "estado": "creado (simulado)"}
        TICKETS.append(t)
        return t

    return [
        Herramienta("buscar_manual", "Busca en el Manual de Ingeniería de FinNorte",
                    {"type": "object", "required": ["consulta"], "properties": {"consulta": {"type": "string", "minLength": 3},
                     "k": {"type": "integer", "minimum": 1, "maximum": 5}}, "additionalProperties": False}, buscar_manual),
        Herramienta("revisar_ventana_despliegue", "Dice si se puede desplegar en una fecha (AAAA-MM-DD) según el riesgo",
                    {"type": "object", "required": ["fecha", "riesgo"], "properties": {"fecha": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
                     "riesgo": {"enum": ["alto", "medio", "bajo"]}}, "additionalProperties": False}, revisar_ventana_despliegue),
        Herramienta("crear_ticket_cambio", "Crea un ticket de cambio en el sistema de gestión de cambios",
                    {"type": "object", "required": ["titulo", "riesgo", "fecha"], "properties": {"titulo": {"type": "string", "minLength": 5},
                     "riesgo": {"enum": ["alto", "medio", "bajo"]}, "fecha": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"}},
                     "additionalProperties": False}, crear_ticket_cambio, sensible=True),
    ]
