---
id: doc-04
titulo: Convenciones de nombres
clasificacion: interna
vigente: si
version: 2025-12
---
Rutas: sustantivos en plural, kebab-case, con versión: /v1/cuentas-ahorro/{cuenta_id}/movimientos.

Campos JSON: snake_case (monto_centavos, fecha_creacion). Fechas en ISO 8601 con zona horaria.

Montos: siempre en centavos enteros con el sufijo _centavos.

operationId: verbo + recurso en camelCase (crearTransferencia, listarMovimientos).
