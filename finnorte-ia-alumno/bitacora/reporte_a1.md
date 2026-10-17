# Reporte Actividad 1 (A1): Buscador Semántico vs. Palabras Clave
- **Curso:** LSCA2318
- **Variante:** `v5-triage` (Triage de incidentes)
- **Proveedor de Embeddings:** `gemini / gemini-embedding-001`

## 1. Cálculo de Similitud Coseno a Mano
Vectores (dimensiones: `[seguridad, despliegue, pruebas, dinero]`):
- **F1:** `[0.9, 0.1, 0.0, 0.2]` -> Norma $\Vert{}F_1\Vert{} = \sqrt{0.81 + 0.01 + 0 + 0.04} = \sqrt{0.86} \approx 0.9274$
- **F2:** `[0.95, 0.05, 0.1, 0.1]` -> Norma $\Vert{}F_2\Vert{} = \sqrt{0.9025 + 0.0025 + 0.01 + 0.01} = \sqrt{0.925} \approx 0.9618$
- **F3:** `[0.1, 0.9, 0.2, 0.3]` -> Norma $\Vert{}F_3\Vert{} = \sqrt{0.01 + 0.81 + 0.04 + 0.09} = \sqrt{0.95} \approx 0.9747$

- **Similitud F1 y F2 (mismo tema: seguridad):**
  - Producto punto: $(0.9)(0.95) + (0.1)(0.05) + (0.0)(0.1) + (0.2)(0.1) = 0.88$
  - $\cos(F_1, F_2) = 0.88 / (0.9274 \times 0.9618) \approx \mathbf{0.987}$
- **Similitud F1 y F3 (temas distintos: seguridad vs. despliegue):**
  - Producto punto: $(0.9)(0.1) + (0.1)(0.9) + (0.0)(0.2) + (0.2)(0.3) = 0.24$
  - $\cos(F_1, F_3) = 0.24 / (0.9274 \times 0.9747) \approx \mathbf{0.266}$

## 2. Resultados en Corpus Común (`bitacora/s1_comparacion.json`)
- Consulta `"subí una contraseña al repo"`: Búsqueda semántica recupera `ing-02#1` (`0.708`) e `ing-02#0` (`0.693`); palabras clave (`--palabras`) no devuelve resultados por falta de coincidencia léxica exacta.
- **Vector (`hash` sin red):** `acierto@1 = 2/10`, `acierto@3 = 4/10`
- **Palabras clave (`BM25`):** `acierto@1 = 4/10`, `acierto@3 = 6/10`
- **Vector (`gemini-embedding-001`):** `acierto@1 = 9/10`, `acierto@3 = 10/10`

## 3. Resultados en Variante `v5-triage` (`bitacora/a1_v5_comparacion.json`)
Evaluación sobre los 10 casos diseñados en `evals/a1_v5-triage.jsonl` contra `corpus/v5-triage`:
- **Vector (`gemini-embedding-001`):** `acierto@1 = 8/10`, `acierto@3 = 10/10`
- **Palabras clave (`BM25`):** `acierto@1 = 7/10`, `acierto@3 = 9/10`

## 4. Conclusiones
- **Cuándo gana Búsqueda Semántica:** Cuando el usuario describe síntomas o incidentes mediante paráfrasis sin usar los términos técnicos exactos del runbook (ej. caso `a01` sobre agotamiento de conexiones en BD, donde el vector acierta en top-1 con `rb-03` y palabras clave falla, logrando además `10/10` en `acierto@3`).
- **Cuándo gana o empata Palabras Clave:** Cuando la consulta contiene IDs exactos de documentos (`rb-03`, `rb-04`, `pm-01`, `pm-03`) o códigos de error literales de los logs (`QueuePool`, `OOMKilled`, `CERTIFICATE_VERIFY_FAILED`).
