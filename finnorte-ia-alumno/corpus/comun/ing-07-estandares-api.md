---
id: ing-07
titulo: Estándares de API
clasificacion: interna
vigente: si
version: 2025-12
---
Las APIs de FinNorte son REST sobre HTTPS y usan JSON.

Versionado: la versión mayor va en la ruta (/v1/, /v2/). Un cambio incompatible requiere versión nueva; la anterior se mantiene al menos 6 meses después de anunciar su retiro.

Errores: se responden con el formato application/problem+json, con los campos type, title, status, detail y trace_id. Nunca se incluyen trazas de pila ni datos personales en el detalle.

Paginación: por cursor (parámetros cursor y limit; limit máximo 100).

Límite de uso: 100 solicitudes por minuto por cliente de API; al excederlo se responde 429 con el encabezado Retry-After.

Idempotencia: las operaciones que mueven dinero exigen el encabezado Idempotency-Key; una misma llave en 24 horas devuelve el mismo resultado sin repetir la operación.

Autenticación: OAuth 2.0 con tokens de acceso de 15 minutos de vigencia.
