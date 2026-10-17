---
id: rb-02
titulo: Runbook: latencia alta en API de transferencias
clasificacion: interna
vigente: si
version: 2026-03
---
Síntoma: alerta "transferencias p95 > 800 ms" o quejas de lentitud.

Revisar en orden:
1. ¿Hubo despliegue en los últimos 60 minutos? Si sí, considerar reversa inmediata (ver rb-08).
2. Latencia del proveedor SPEI (panel spei-gateway): si sube igual, ver rb-05.
3. Conexiones de base de datos (pool en uso > 90 %): ver rb-03.
4. CPU y memoria de los pods de pagos-api: si están saturados, escalar réplicas de 6 a 12.

No reiniciar todos los pods a la vez: se reinician de uno en uno.
