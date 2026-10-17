---
id: api-04
titulo: Transferencias
clasificacion: publica
vigente: si
version: 2026-04
---
POST /v1/transferencias crea una transferencia SPEI. Scope transferencias:crear.

Cuerpo: cuenta_origen, clabe_destino (18 dígitos), monto_centavos (entero > 0), concepto (máximo 40 caracteres), referencia_numerica (7 dígitos).

Encabezado obligatorio: Idempotency-Key (UUID). Repetir con la misma llave y el mismo cuerpo en 24 horas devuelve la misma transferencia (200). La misma llave con un cuerpo distinto devuelve 409 con el código FN-4091.

Estados: pendiente → liquidada, o pendiente → rechazada. Una liquidada puede pasar a devuelta si el banco destino la regresa.

La respuesta inicial es 202 con estado pendiente. El estado final se notifica por webhook o se consulta con GET /v1/transferencias/{id}.
