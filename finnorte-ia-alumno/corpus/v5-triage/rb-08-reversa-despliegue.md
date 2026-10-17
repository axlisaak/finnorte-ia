---
id: rb-08
titulo: Runbook: reversa de un despliegue
clasificacion: interna
vigente: si
version: 2026-03
---
Criterio: si los errores 5xx o la latencia empeoran en los 60 minutos posteriores a un despliegue, la primera acción es revertir; se investiga después.

Cómo: en la herramienta de despliegue, seleccionar la versión anterior y desplegar con estrategia inmediata. Verificar que los errores bajen en 10 minutos.

Las migraciones de base de datos deben tener script de reversa; si no lo tienen, escalar al DBA antes de revertir.
