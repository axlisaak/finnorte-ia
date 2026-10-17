---
id: rb-03
titulo: Runbook: conexiones a base de datos agotadas
clasificacion: interna
vigente: si
version: 2026-02
---
Síntoma en logs: "QueuePool limit of size 20 overflow 10 reached" o "remaining connection slots are reserved".

Causas comunes: consultas lentas que retienen conexiones, una fuga de conexiones tras un despliegue o un pico de tráfico.

Acciones: identificar consultas de más de 5 s en el monitor de la base de datos y cancelarlas si son de reportes; si coincide con un despliegue, revertir (rb-08). No aumentar el tamaño del pool sin aprobación del DBA: puede saturar la base de datos.

Severidad típica: SEV2; SEV1 si las transferencias fallan.
