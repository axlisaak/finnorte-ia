# Bitácora de uso de IA

> Obligatoria en todas las entregas. Una fila por uso relevante de una herramienta de IA (chat, asistente de código, generador).
> La IA es una herramienta permitida; ocultarla no lo es. Se califica la honestidad y la calidad de la validación, no si la usaste.

| Fecha | Entrega | Herramienta y modelo | Para qué la usé | Prompt (resumen o enlace) | Qué acepté | Qué cambié o rechacé y por qué | Cómo lo validé |
|---|---|---|---|---|---|---|---|
| 2026-10-16 | A1 | Gemini | Implementar funciones `normalizar`, `coseno` y `buscar` en `retrieval.py` | "Ayúdame a implementar normalizar, coseno y buscar para pasar test_a1_vectores" | El cálculo matricial con `np.linalg.norm`, `np.where` para evitar división por cero y ordenamiento con `np.argsort` | La primera versión de `buscar` devolvía una tupla `(fragmento, puntaje)` y fallaba con `AttributeError`; la cambié para devolver objetos `Resultado(fragmento, puntaje)` | Ejecutando `pytest -q` (10 passed, incluyendo los 4 tests de `test_a1_vectores.py`) |
| 2026-10-16 | A1 | Gemini | Redactar los 10 casos de evaluación de `v5-triage` y script de comparación | "Generar 10 preguntas en `evals/a1_v5-triage.jsonl` basadas en `corpus/v5-triage` y evaluar acierto@1 y acierto@3" | 6 preguntas de paráfrasis de síntomas de incidentes y 4 preguntas con IDs de runbooks/postmortems | Corregí la codificación del archivo `.jsonl` de UTF-8 con BOM a UTF-8 limpio porque `json.loads` lanzaba `JSONDecodeError` | Ejecutando `python guia/s1_v5.py` y verificando la generación de `bitacora/a1_v5_comparacion.json` |
