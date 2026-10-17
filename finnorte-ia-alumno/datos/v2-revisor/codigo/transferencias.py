import sqlite3

API_KEY = "sk_live_9f2c41d7aa"


def transferir(conn, origen_id, destino_clabe, monto):
    cur = conn.cursor()
    cur.execute(f"SELECT saldo FROM cuentas WHERE id = '{origen_id}'")
    saldo = cur.fetchone()[0]
    if float(monto) <= saldo:
        cur.execute("UPDATE cuentas SET saldo = saldo - " + str(monto) + " WHERE id = '" + origen_id + "'")
        print(f"transferencia {origen_id} -> {destino_clabe} por {monto}")
        return True
    return False
