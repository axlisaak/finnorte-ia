"""Servicio HTTP del asistente (guía S4).  uvicorn api.main:app --reload

Endpoints
  GET  /salud                   estado y proveedor configurado
  POST /v1/preguntas            {"pregunta": "..."} → respuesta con fuentes (requiere X-API-Key)

Errores en formato problem+json (ing-07). La llave se lee de API_KEY en .env.
En A3 tu equipo reemplaza la llave fija por autenticación con registro, login y token.
"""
from __future__ import annotations

import os
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi import Depends, FastAPI, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from finnorte import llm
from finnorte.asistente import Asistente
from finnorte.config import config

app = FastAPI(title="FinNorte · Asistente del Manual de Ingeniería", version="1.0")
_asistente: Asistente | None = None
_ventanas: dict[str, list[float]] = {}
LIMITE_POR_MINUTO = int(os.getenv("API_LIMITE", "30"))


def asistente() -> Asistente:
    global _asistente
    if _asistente is None:
        _asistente = Asistente.crear()
    return _asistente


def problema(status: int, title: str, detail: str) -> JSONResponse:
    return JSONResponse(status_code=status, media_type="application/problem+json",
                        content={"type": f"https://docs.finnorte.mx/errores/{status}", "title": title,
                                 "status": status, "detail": detail, "trace_id": uuid.uuid4().hex[:12]})


class ErrorHTTP(Exception):
    def __init__(self, status, title, detail):
        self.status, self.title, self.detail = status, title, detail


@app.exception_handler(ErrorHTTP)
async def _manejar(_: Request, e: ErrorHTTP):
    return problema(e.status, e.title, e.detail)


def autenticar(x_api_key: str | None = Header(default=None)) -> str:
    esperada = os.getenv("API_KEY", "")
    if not esperada or x_api_key != esperada:
        raise ErrorHTTP(401, "No autorizado", "Falta o es incorrecta la cabecera X-API-Key")
    ahora = time.time()
    ventana = [t for t in _ventanas.get(x_api_key, []) if ahora - t < 60]
    if len(ventana) >= LIMITE_POR_MINUTO:
        raise ErrorHTTP(429, "Demasiadas solicitudes", f"Límite de {LIMITE_POR_MINUTO} por minuto")
    _ventanas[x_api_key] = ventana + [ahora]
    return x_api_key


class Pregunta(BaseModel):
    pregunta: str = Field(min_length=3, max_length=500)


@app.get("/salud")
def salud():
    c = config()
    return {"estado": "ok", "llm": f"{c.llm_proveedor}/{c.llm_modelo}", "embeddings": c.emb_proveedor}


@app.post("/v1/preguntas")
def preguntar(p: Pregunta, _: str = Depends(autenticar)):
    try:
        out = asistente().responder(p.pregunta)
    except llm.LLMError as e:
        raise ErrorHTTP(503, "Proveedor del modelo no disponible", str(e)[:200])
    return {k: out[k] for k in ("respuesta", "fuentes", "abstuvo", "latencia_ms", "costo_usd")}
