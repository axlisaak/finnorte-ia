---
id: sec-01
titulo: Secretos fuera del código
clasificacion: interna
vigente: si
version: 2026-02
---
Regla SEC-01: ningún secreto (llave de API, contraseña, token, certificado privado) se escribe en el código ni en archivos versionados. Se leen del gestor de secretos o de variables de entorno inyectadas en tiempo de ejecución.

Señales en revisión: asignaciones como API_KEY = "...", password = "...", cadenas que empiezan con sk_, AKIA o -----BEGIN.

Severidad: crítica. Corrección: mover a os.environ o al cliente de la bóveda y revocar el secreto expuesto.
