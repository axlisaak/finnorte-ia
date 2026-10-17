---
id: sec-06
titulo: Criptografía y aleatoriedad
clasificacion: interna
vigente: si
version: 2026-02
---
Regla SEC-06: contraseñas con PBKDF2, bcrypt o Argon2 y sal por usuario; nunca MD5, SHA-1 ni SHA-256 sin sal. Tokens y códigos de un solo uso con el módulo secrets, nunca con random. Comparación de secretos con hmac.compare_digest.

Severidad: crítica para contraseñas en claro o con MD5/SHA-1; alta para random en tokens.
