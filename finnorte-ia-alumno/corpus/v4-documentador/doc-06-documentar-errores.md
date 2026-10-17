---
id: doc-06
titulo: Cómo documentar errores
clasificacion: interna
vigente: si
version: 2026-01
---
Cada error documentado incluye: código HTTP, código interno (si existe), cuándo ocurre (condición concreta) y qué debe hacer quien llama (corregir la entrada, reintentar con espera, contactar a soporte con el trace_id).

Los errores se extraen del código: cada raise HTTPException o respuesta de error debe aparecer en la documentación, y la documentación no debe listar errores que el código no produce.
