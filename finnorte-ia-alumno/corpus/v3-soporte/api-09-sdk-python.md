---
id: api-09
titulo: SDK de Python
clasificacion: publica
vigente: si
version: 2026-05
---
Instalación: pip install finnorte-sdk (versión 2.x; la 1.x no soporta los endpoints v2).

Ejemplo:
from finnorte import Cliente
cli = Cliente(client_id=..., client_secret=..., ambiente="sandbox")
t = cli.transferencias.crear(cuenta_origen="cta_123", clabe_destino="...", monto_centavos=150000, concepto="Pago factura 88", idempotency_key=uuid4())

El SDK renueva el token automáticamente, reintenta 429 y 503 respetando Retry-After y genera la Idempotency-Key si no se proporciona.
