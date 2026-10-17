---
id: rb-06
titulo: Runbook: cola de notificaciones atascada
clasificacion: interna
vigente: si
version: 2025-11
---
Síntoma: la métrica notificaciones.cola.pendientes crece sin bajar; logs con "consumer lag" o "message processing failed, will retry".

Acciones: revisar si un mensaje "venenoso" falla repetidamente (mismo message_id en los errores) y moverlo a la cola de mensajes muertos; escalar consumidores de 2 a 6.

Severidad típica: SEV3 (no afecta dinero).
