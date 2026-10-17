---
id: ing-12
titulo: Monitoreo, SLO y alertas
clasificacion: interna
vigente: si
version: 2026-03
---
Objetivos de nivel de servicio (SLO):
- API de transferencias: disponibilidad mensual de 99.9 % y latencia p95 menor a 800 ms.
- API de consultas (saldos y movimientos): disponibilidad de 99.5 % y latencia p95 menor a 1,200 ms.

Presupuesto de error: si en un mes se consume más del 50 % del presupuesto de error, se congelan los cambios de riesgo medio y alto del servicio hasta recuperar la estabilidad.

Alertas: cada alerta debe tener un runbook enlazado que diga qué revisar primero. Una alerta que se dispara más de 5 veces en una semana sin acción se revisa o se elimina.

Registros: todos los servicios escriben registros estructurados en JSON con trace_id, nivel, servicio y mensaje, sin datos restringidos.
