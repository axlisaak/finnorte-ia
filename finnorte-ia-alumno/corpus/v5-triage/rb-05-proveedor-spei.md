---
id: rb-05
titulo: Runbook: proveedor SPEI lento o caído
clasificacion: interna
vigente: si
version: 2026-03
---
Síntoma en logs: "spei-gateway timeout after 30000ms", respuestas 503 del gateway o FN-5031 en aumento.

Acciones: confirmar en el panel de estado del proveedor; activar el modo "encolar transferencias" (se aceptan con estado pendiente y se envían al recuperarse); comunicar a negocio. No reintentar en bucle: el gateway ya reintenta con espera exponencial.

Severidad: SEV1 si no hay modo de encolado disponible; SEV2 si el encolado funciona.
