---
id: ing-06
titulo: Uso de IA generativa en ingeniería
clasificacion: interna
vigente: si
version: 2026-04
---
Herramientas aprobadas: el asistente de código corporativo con licencia empresarial y la API de modelos contratada por FinNorte. Cualquier otra herramienta requiere aprobación de Seguridad.

Qué no se comparte: datos restringidos o confidenciales (ver Clasificación de datos), secretos y código de los módulos antifraude.

Revisión humana: todo código, prueba o documento generado con IA se revisa como si lo hubiera escrito una persona nueva en el equipo. La persona autora del PR responde por él.

Registro: los PR asistidos por IA llevan la etiqueta "asistido-por-ia". Los sistemas que usan modelos en producción registran versión del modelo, versión del prompt, fuentes usadas y resultado de las validaciones.

Sistemas con IA para clientes: deben tener una ruta hacia una persona, no ejecutar operaciones de dinero sin confirmación explícita del cliente y evaluarse antes de cada cambio de modelo o de prompt.
