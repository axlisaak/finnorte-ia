---
id: rb-07
titulo: Runbook: reinicios por memoria (OOMKilled)
clasificacion: interna
vigente: si
version: 2026-01
---
Síntoma: pods reiniciándose con razón OOMKilled; logs que terminan abruptamente; aumento de errores 502 en el balanceador.

Acciones: comparar el uso de memoria antes y después del último despliegue; si creció, revertir (rb-08). Como mitigación temporal, subir el límite de memoria de 512 Mi a 1 Gi con aprobación del líder técnico.

Causa frecuente: cargar resultados completos de consultas en memoria (reportes) o cachés sin límite.
