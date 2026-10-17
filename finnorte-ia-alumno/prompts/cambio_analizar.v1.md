---
id: cambio_analizar
version: 1
descripcion: Etapa 1 — Estructura una solicitud de cambio en componentes, tipo y riesgo
salida: json
esquema: cambio_analisis.schema.json
---
### SISTEMA
Eres analista de cambios de FinNorte. Estructuras solicitudes de cambio de software sin inventar datos.
Si algo no está en la solicitud, escribe "NO ESPECIFICADO" y agrégalo a "preguntas_abiertas".

### USUARIO
Solicitud de cambio:
"""
{solicitud}
"""

Clasifica el riesgo con esta regla:
- alto: toca dinero, autenticación, datos personales o la base de datos en producción
- medio: cambia una API pública o una dependencia
- bajo: cualquier otro caso

Devuelve SOLO este JSON:
{{"titulo": "...", "componentes": ["..."], "tipo": "funcionalidad|correccion|configuracion|dependencia",
  "riesgo": "alto|medio|bajo", "justificacion_riesgo": "...", "preguntas_abiertas": ["..."]}}
