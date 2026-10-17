from fastapi import FastAPI

app = FastAPI()
DB = {}


@app.get("/v1/cuentas/{cuenta_id}/movimientos")
def movimientos(cuenta_id: str, usuario=None):
    # usuario viene del token, ya autenticado
    try:
        return DB[cuenta_id]["movimientos"]
    except Exception:
        pass
