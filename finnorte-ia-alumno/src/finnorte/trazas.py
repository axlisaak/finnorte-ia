"""Bitácora de ejecución en JSONL: una línea por llamada o etapa.

Es la evidencia que piden todas las entregas: qué prompt (y qué versión) se usó,
con qué modelo, cuánto tardó, cuántos tokens consumió y cuánto costó.
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

from .config import config

_SESION = uuid.uuid4().hex[:8]


def archivo_trazas() -> Path:
    d = config().dir_trazas
    d.mkdir(parents=True, exist_ok=True)
    return d / "trazas.jsonl"


def registrar(tipo: str, **datos: Any) -> dict:
    """Agrega un evento a bitacora/trazas.jsonl y lo devuelve."""
    evento = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "sesion": _SESION, "tipo": tipo, **datos}
    with archivo_trazas().open("a", encoding="utf-8") as f:
        f.write(json.dumps(evento, ensure_ascii=False, default=str) + "\n")
    return evento


def leer(tipo: str | None = None) -> list[dict]:
    p = archivo_trazas()
    if not p.exists():
        return []
    eventos = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
    return [e for e in eventos if tipo is None or e.get("tipo") == tipo]
