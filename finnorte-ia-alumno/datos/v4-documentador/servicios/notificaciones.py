"""Envío de notificaciones push y correo."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Notificacion(BaseModel):
    cliente_id: str
    canal: str          # "push" o "correo"
    plantilla: str
    variables: dict = {}


@app.post("/v1/notificaciones", status_code=201)
def enviar(n: Notificacion):
    if n.canal not in ("push", "correo"):
        raise HTTPException(422, "Canal no soportado")
    if n.plantilla not in ("transferencia_enviada", "nuevo_dispositivo", "cambio_contrasena"):
        raise HTTPException(422, "Plantilla desconocida")
    return {"id": "ntf_1", "estado": "encolada"}
