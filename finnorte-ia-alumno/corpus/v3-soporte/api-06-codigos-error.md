---
id: api-06
titulo: Códigos de error
clasificacion: publica
vigente: si
version: 2026-04
---
Los errores usan application/problem+json con un campo adicional code.

- FN-4001 · 422 · CLABE inválida (longitud o dígito verificador).
- FN-4002 · 422 · Fondos insuficientes.
- FN-4003 · 422 · Monto excede el límite por operación del nivel de la cuenta.
- FN-4004 · 422 · Límite diario alcanzado.
- FN-4011 · 401 · Token inválido o expirado.
- FN-4031 · 403 · Scope insuficiente.
- FN-4091 · 409 · Idempotency-Key reutilizada con otro cuerpo.
- FN-4291 · 429 · Límite de tasa excedido.
- FN-5031 · 503 · SPEI no disponible temporalmente; reintentar con espera exponencial.

Todo error incluye trace_id; inclúyelo al contactar a soporte.
