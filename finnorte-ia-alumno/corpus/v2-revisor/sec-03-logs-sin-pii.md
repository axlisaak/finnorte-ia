---
id: sec-03
titulo: Registros sin datos personales
clasificacion: interna
vigente: si
version: 2026-01
---
Regla SEC-03: los registros (logs) no incluyen datos restringidos: contraseñas, tokens, CLABE completa, número de tarjeta, CURP, correo o teléfono completos.

Se permite: identificador interno del cliente, últimos 4 dígitos y trace_id.

Severidad: alta. Corrección: enmascarar antes de escribir o registrar solo el identificador.
