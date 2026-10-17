import requests


def notificar(cliente, monto):
    url = "https://hooks.finnorte.mx/push"
    try:
        requests.post(url, json={"tel": cliente["telefono"], "msg": f"Enviaste {monto}"}, timeout=None)
    except:
        pass
