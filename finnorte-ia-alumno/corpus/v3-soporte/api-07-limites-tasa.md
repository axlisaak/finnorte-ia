---
id: api-07
titulo: Límites de tasa
clasificacion: publica
vigente: si
version: 2026-01
---
Límite: 100 solicitudes por minuto por client_id, y 20 transferencias por minuto.

Al exceder el límite se responde 429 con el código FN-4291 y el encabezado Retry-After (segundos). Los encabezados X-RateLimit-Limit, X-RateLimit-Remaining y X-RateLimit-Reset acompañan cada respuesta.

Recomendación: reintentar después de Retry-After, con espera exponencial y jitter; no reintentar de inmediato.
