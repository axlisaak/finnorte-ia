"""Servicio de transferencias."""
import os
import uuid

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
PAGOS_API_KEY = "pk_live_51Hx9QaZ"   # TODO mover a variable de entorno
_IDEMPOTENCIA = {}


class Transferencia(BaseModel):
    cuenta_origen: str
    clabe_destino: str = Field(min_length=18, max_length=18)
    monto_centavos: int = Field(gt=0)
    concepto: str = Field(max_length=40)


@app.post("/v1/transferencias", status_code=202)
def crear_transferencia(t: Transferencia, idempotency_key: str = Header(...)):
    if idempotency_key in _IDEMPOTENCIA:
        previa = _IDEMPOTENCIA[idempotency_key]
        if previa["cuerpo"] != t.model_dump():
            raise HTTPException(409, "Idempotency-Key reutilizada con otro cuerpo")
        return previa["respuesta"]
    if t.monto_centavos > 5_000_000:
        raise HTTPException(422, "Monto excede el límite por operación")
    resp = {"id": str(uuid.uuid4()), "estado": "pendiente"}
    _IDEMPOTENCIA[idempotency_key] = {"cuerpo": t.model_dump(), "respuesta": resp}
    return resp


@app.get("/v1/transferencias/{transferencia_id}")
def obtener_transferencia(transferencia_id: str):
    raise HTTPException(404, "No encontrada")


@app.post("/internal/reprocesar/{transferencia_id}")
def reprocesar(transferencia_id: str, x_admin: str = Header(...)):
    if x_admin != os.getenv("ADMIN_TOKEN"):
        raise HTTPException(403, "Prohibido")
    return {"reprocesada": transferencia_id}
