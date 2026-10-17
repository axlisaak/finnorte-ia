---
id: doc-03
titulo: Plantilla y reglas para especificaciones OpenAPI
clasificacion: interna
vigente: si
version: 2026-03
---
Versión: OpenAPI 3.1.0. Campos obligatorios en info: title, version, description y contact.

Cada operación lleva: summary (máximo 10 palabras), description, operationId en camelCase y único, tags, y al menos una respuesta de éxito y las respuestas 4xx que el código produce.

Errores: las respuestas de error usan el esquema Problem (type, title, status, detail, trace_id) con media type application/problem+json.

Seguridad: se declara en components.securitySchemes y se aplica por operación. Cada esquema de request y response incluye un example con datos sintéticos.

La especificación debe validar sin errores con un validador OpenAPI antes de publicarse.
