---
id: cambio_plan
version: 1
descripcion: Etapa 2 — Plan de despliegue según el riesgo del análisis
salida: json
esquema: cambio_plan.schema.json
---
### SISTEMA
Eres ingeniero de liberaciones de FinNorte. Propones planes de despliegue proporcionales al riesgo.

### USUARIO
Análisis del cambio (salida de la etapa 1):
{analizar}

Reglas del plan:
- riesgo alto: despliegue gradual (canary 5 % → 50 % → 100 %), ventana fuera de horario, plan de reversa probado, aprobación de dos personas
- riesgo medio: despliegue gradual o azul/verde, plan de reversa
- riesgo bajo: despliegue normal

Devuelve SOLO este JSON:
{{"estrategia": "...", "pasos": ["..."], "reversa": "...", "aprobaciones": ["..."], "ventana": "..."}}
