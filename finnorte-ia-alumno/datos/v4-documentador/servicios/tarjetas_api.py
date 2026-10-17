"""Bloqueo y desbloqueo de tarjetas."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
TARJETAS = {"tar_9": {"estado": "activa"}}


class Bloqueo(BaseModel):
    motivo: str   # "temporal" | "robo" | "extravio"


@app.post("/v1/tarjetas/{tarjeta_id}/bloqueo")
def bloquear(tarjeta_id: str, b: Bloqueo):
    if tarjeta_id not in TARJETAS:
        raise HTTPException(404, "Tarjeta no encontrada")
    if b.motivo not in ("temporal", "robo", "extravio"):
        raise HTTPException(422, "Motivo inválido")
    TARJETAS[tarjeta_id]["estado"] = "bloqueada_" + b.motivo
    return {"tarjeta_id": tarjeta_id, "estado": TARJETAS[tarjeta_id]["estado"]}


@app.delete("/v1/tarjetas/{tarjeta_id}/bloqueo")
def desbloquear(tarjeta_id: str):
    t = TARJETAS.get(tarjeta_id)
    if not t:
        raise HTTPException(404, "Tarjeta no encontrada")
    if t["estado"] != "bloqueada_temporal":
        raise HTTPException(409, "Solo se puede desbloquear un bloqueo temporal")
    t["estado"] = "activa"
    return {"tarjeta_id": tarjeta_id, "estado": "activa"}
