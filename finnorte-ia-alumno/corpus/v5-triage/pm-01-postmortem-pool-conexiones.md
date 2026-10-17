---
id: pm-01
titulo: Postmortem 2026-03-14: conexiones agotadas tras despliegue
clasificacion: interna
vigente: si
version: 2026-03
---
Resumen: de 13:05 a 13:52 el 38 % de las transferencias falló con error 500. Severidad SEV1.

Causa raíz: la versión 4.12 de pagos-api abría una conexión nueva por solicitud en el endpoint de comisiones y no la cerraba (fuga de conexiones). El pool se agotó a los 20 minutos del despliegue.

Detección: alerta de errores 5xx a las 13:09. Se revirtió a las 13:40; la recuperación terminó a las 13:52.

Qué falló: la prueba de carga no se corrió antes del despliegue. Acciones: prueba de carga obligatoria en el pipeline para cambios en pagos-api (responsable: plataforma, fecha: 2026-04-15).
