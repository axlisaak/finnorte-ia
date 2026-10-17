---
id: api-08
titulo: Versionado y deprecaciones
clasificacion: publica
vigente: si
version: 2026-06
---
La versión mayor va en la ruta. Un cambio incompatible crea una versión nueva; la anterior se mantiene al menos 6 meses tras el anuncio.

Deprecaciones vigentes:
- GET /v1/saldos fue retirado el 30 de junio de 2026. Usar GET /v2/cuentas/{cuenta_id}/saldo (el monto ahora viene en centavos).
- GET /v1/cuentas/{id} se retira el 31 de diciembre de 2026. Usar /v2/cuentas/{id}.

Las respuestas de endpoints deprecados incluyen el encabezado Sunset con la fecha de retiro.
