"""Consulta de tipo de cambio FIX (cache de 10 minutos)."""
import time

from fastapi import FastAPI

app = FastAPI()
_CACHE = {"valor": None, "ts": 0}


@app.get("/v1/tipo-cambio/usd-mxn")
def tipo_cambio():
    if time.time() - _CACHE["ts"] > 600:
        _CACHE.update(valor=18.42, ts=time.time())   # simulado
    return {"par": "USD/MXN", "valor": _CACHE["valor"], "fuente": "FIX simulado"}
