---
id: ing-02
titulo: Manejo de secretos
clasificacion: interna
vigente: si
version: 2026-02
---
Un secreto es cualquier credencial que da acceso: llaves de API, contraseñas de bases de datos, certificados privados y tokens de servicio.

Dónde viven: los secretos se guardan únicamente en el gestor de secretos corporativo (bóveda). Está prohibido guardarlos en el repositorio, en archivos de configuración versionados, en variables de un pipeline sin cifrar o en mensajes de chat.

Rotación: los secretos de producción se rotan cada 30 días. Los de ambientes no productivos, cada 90 días. La rotación es automática siempre que el servicio lo permita.

Si un secreto se expone (por ejemplo, se sube a un repositorio, aunque sea privado): se revoca en máximo 1 hora desde que se detecta, se abre un incidente de severidad 2 y se revisa el historial de uso del secreto en los últimos 30 días. Borrar el commit no es suficiente: el secreto queda en el historial.

Cada repositorio debe tener activado el escaneo de secretos en el pipeline de integración continua; un hallazgo bloquea el merge.
