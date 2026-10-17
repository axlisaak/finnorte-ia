---
id: api-02
titulo: Autenticación OAuth 2.0
clasificacion: publica
vigente: si
version: 2026-03
---
La API usa OAuth 2.0 con el flujo client credentials.

Solicitar token: POST /oauth/token con grant_type=client_credentials, client_id y client_secret, y el parámetro scope.

Scopes: cuentas:leer, transferencias:crear, transferencias:leer, webhooks:administrar.

El token de acceso dura 15 minutos (expires_in = 900). No hay refresh token en este flujo: al expirar, se solicita uno nuevo. Se envía en el encabezado Authorization: Bearer <token>.

Un token expirado o con scope insuficiente devuelve 401 (expirado o inválido) o 403 (scope insuficiente).
