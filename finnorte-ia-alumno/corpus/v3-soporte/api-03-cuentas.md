---
id: api-03
titulo: Endpoints de cuentas
clasificacion: publica
vigente: si
version: 2026-03
---
GET /v2/cuentas/{cuenta_id} — datos de la cuenta (nivel, estado, últimos 4 dígitos de la CLABE). Scope cuentas:leer.

GET /v2/cuentas/{cuenta_id}/saldo — saldo disponible y saldo retenido, en centavos (enteros) y moneda MXN.

GET /v2/cuentas/{cuenta_id}/movimientos?desde=AAAA-MM-DD&hasta=AAAA-MM-DD&limit=50&cursor=... — movimientos paginados por cursor; limit máximo 100. El rango máximo entre desde y hasta es de 90 días.

Solo se pueden consultar cuentas vinculadas al socio; otra cuenta devuelve 404 (no 403, para no revelar que existe).
