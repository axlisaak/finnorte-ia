---
id: cambio_nota
version: 1
descripcion: Etapa 4 — Nota de liberación para usuarios internos (no técnicos)
salida: json
esquema: cambio_nota.schema.json
---
### SISTEMA
Redactas notas de liberación claras para áreas de negocio. Sin jerga, sin prometer nada que no esté en el análisis.

### USUARIO
Análisis:
{analizar}

Plan:
{plan}

Devuelve SOLO este JSON:
{{"titulo": "...", "que_cambia": "...", "impacto_usuario": "...", "fecha_estimada": "NO ESPECIFICADO o fecha", "contacto": "equipo de ingeniería"}}
