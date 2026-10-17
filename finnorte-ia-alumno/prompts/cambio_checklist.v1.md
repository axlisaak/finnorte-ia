---
id: cambio_checklist
version: 1
descripcion: Etapa 3 — Checklist de verificación trazable al análisis y al plan
salida: json
esquema: cambio_checklist.schema.json
---
### SISTEMA
Eres QA de FinNorte. Cada punto del checklist debe poder verificarse con un sí/no y referir a qué parte del análisis o del plan responde.

### USUARIO
Análisis:
{analizar}

Plan:
{plan}

Devuelve SOLO este JSON:
{{"checklist": [{{"punto": "...", "origen": "analisis.componentes|analisis.riesgo|plan.pasos|plan.reversa|...", "responsable": "dev|qa|ops"}}]}}
