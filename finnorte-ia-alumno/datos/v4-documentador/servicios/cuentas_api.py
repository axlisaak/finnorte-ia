"""Consulta de cuentas y saldos."""
from datetime import date

from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
CUENTAS = {"cta_123": {"nivel": 2, "saldo_centavos": 1250000, "clabe": "646180000000000000"}}


@app.get("/v2/cuentas/{cuenta_id}/saldo")
def saldo(cuenta_id: str):
    c = CUENTAS.get(cuenta_id)
    if not c:
        raise HTTPException(404, "Cuenta no encontrada")
    return {"cuenta_id": cuenta_id, "saldo_centavos": c["saldo_centavos"], "moneda": "MXN"}


@app.get("/v2/cuentas/{cuenta_id}/movimientos")
def movimientos(cuenta_id: str, desde: date, hasta: date, limit: int = Query(50, le=100), cursor: str | None = None):
    if (hasta - desde).days > 90:
        raise HTTPException(422, "El rango máximo es de 90 días")
    if cuenta_id not in CUENTAS:
        raise HTTPException(404, "Cuenta no encontrada")
    return {"movimientos": [], "siguiente_cursor": None}
