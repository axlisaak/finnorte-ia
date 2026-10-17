@'
# Reporte Actividad 1 (A1): Buscador Semántico vs. Palabras Clave
- **Curso:** LSCA2318 - Tópico selecto de tecnologías de la información
- **Variante:** `v5-triage` (Triage de incidentes)
- **Proveedor de Embeddings:** `gemini` (`gemini-embedding-001`)

---

## 1. Implementación de Vectores (`test_a1`) — [25 pts]
Se implementaron las tres funciones núcleo en `src/finnorte/retrieval.py`:
- **`normalizar(m)`:** Calcula la norma L2 por fila (`np.linalg.norm(m, axis=1, keepdims=True)`) y divide cada vector entre su norma, utilizando `np.where(n == 0, 1, n)` para evitar división por cero en vectores nulos (validado con `test_normalizar_vector_cero`).
- **`coseno(a, b)`:** Convierte las entradas a arreglos flotantes, calcula sus normas `na` y `nb`, retorna `0.0` si alguna es cero y calcula `float(a @ b / (na * nb))` en caso contrario.
- **`buscar(self, consulta, k=3)`:** Genera el embedding de la consulta con `embed([consulta])`, lo normaliza, calcula el producto punto matricial `s = self.matriz @ q` (equivalente a la similitud coseno de todos los fragmentos a la vez), ordena de mayor a menor con `np.argsort(-s)[:k]` y devuelve los objetos `Resultado(fragmento, puntaje)`.
- **Evidencia:** Ejecución de `pytest -q` con **4 de 4 pruebas de `test_a1_vectores.py` en verde** (`10 passed` en total en la suite inicial) y configuración de `VARIANTE = "v5-triage"` en `src/finnorte/variante.py`.

---

## 2. Embeddings Manuales (Cálculo de Coseno a Mano) — [15 pts]
Dados los vectores en 4 dimensiones (`[seguridad, despliegue, pruebas, dinero]`) de `guia/s1_buscador.py`:
- **F1** ("Rotar las llaves de API cada 30 días"): `[0.9, 0.1, 0.0, 0.2]`
- **F2** ("Revocar un secreto expuesto en el repositorio"): `[0.95, 0.05, 0.1, 0.1]`
- **F3** ("Desplegar con canary los martes en la noche"): `[0.1, 0.9, 0.2, 0.3]`

### a) Normas L2 ($\Vert{}v\Vert{} = \sqrt{\sum v_i^2}$):
- $\Vert{}F_1\Vert{} = \sqrt{0.9^2 + 0.1^2 + 0.0^2 + 0.2^2} = \sqrt{0.81 + 0.01 + 0 + 0.04} = \sqrt{0.86} \approx \mathbf{0.9274}$
- $\Vert{}F_2\Vert{} = \sqrt{0.95^2 + 0.05^2 + 0.1^2 + 0.1^2} = \sqrt{0.9025 + 0.0025 + 0.01 + 0.01} = \sqrt{0.925} \approx \mathbf{0.9618}$
- $\Vert{}F_3\Vert{} = \sqrt{0.1^2 + 0.9^2 + 0.2^2 + 0.3^2} = \sqrt{0.01 + 0.81 + 0.04 + 0.09} = \sqrt{0.95} \approx \mathbf{0.9747}$

### b) Similitud coseno F1–F2 (mismo tema: seguridad):
- Producto punto: $F_1 \cdot F_2 = (0.9)(0.95) + (0.1)(0.05) + (0.0)(0.1) + (0.2)(0.1) = 0.855 + 0.005 + 0 + 0.02 = \mathbf{0.88}$
- $\cos(F_1, F_2) = \frac{0.88}{0.9274 \times 0.9618} = \frac{0.88}{0.8919} \approx \mathbf{0.987}$ (coincide con el valor `0.987` impreso por `guia/s1_buscador.py`).

### c) Similitud coseno F1–F3 (temas distintos: seguridad vs. despliegue):
- Producto punto: $F_1 \cdot F_3 = (0.9)(0.1) + (0.1)(0.9) + (0.0)(0.2) + (0.2)(0.3) = 0.09 + 0.09 + 0 + 0.06 = \mathbf{0.24}$
- $\cos(F_1, F_3) = \frac{0.24}{0.9274 \times 0.9747} = \frac{0.24}{0.9039} \approx \mathbf{0.266}$ (coincide con el valor `0.266` impreso por `guia/s1_buscador.py`).

---

## 3. Comparación Semántico vs. Palabras Clave — [25 pts]

### a) Prueba puntual en terminal (`ing-02`):
- `python -m finnorte buscar "subí una contraseña al repo"` -> Recupera `ing-02#1` (`0.708`) e `ing-02#0` (`0.693`, *Manejo de secretos*), porque el embedding asocia semánticamente "contraseña" con "secreto/llave".
- `python -m finnorte buscar "subí una contraseña al repo" --palabras` -> No devuelve resultados porque `ing-02` no contiene la palabra literal "contraseña".

### b) Evaluación en Corpus Común (`corpus/comun`, evidencia en `bitacora/s1_comparacion.json`):
| Método / Proveedor | Acierto@1 | Acierto@3 | Explicación |
| :--- | :---: | :---: | :--- |
| **Vector (`EMB_PROVIDER=hash`)** | 2/10 | 4/10 | El hash pseudoaleatorio solo sirve para correr pruebas sin red; no captura significado ni sinónimos. |
| **Palabras clave (BM25)** | 4/10 | 6/10 | Solo acierta cuando la consulta comparte palabras exactas con el documento. |
| **Vector (`gemini-embedding-001`)** | **9/10** | **10/10** | Entiende sinónimos y paráfrasis con alta precisión. |

### c) Evaluación en Variante `v5-triage` (`corpus/v5-triage`, evidencia en `evals/a1_v5-triage.jsonl` y `bitacora/a1_v5_comparacion.json`):
| Método | Acierto@1 | Acierto@3 |
| :--- | :---: | :---: |
| **Búsqueda Semántica (`vector` - Gemini)** | **8/10** | **10/10** |
| **Búsqueda por Palabras Clave (`palabras` - BM25)** | **7/10** | **9/10** |

---

## 4. Análisis Conceptual y Componentes — [15 pts]
El sistema de recuperación construido en FinNorte se compone de cuatro piezas fundamentales:
1. **Fragmentación e ingesta (`corpus/` -> `Fragmento`):** Los documentos Markdown de `corpus/comun` y `corpus/v5-triage` se dividen en fragmentos manejables con metadatos (`doc_id`, `titulo`, clasificación y vigencia) para recuperar pasajes específicos en lugar de documentos enteros.
2. **Representación vectorial (`src/finnorte/embeddings.py`):** Transforma texto en vectores densos mediante `gemini-embedding-001` (con caché en `bitacora/emb_*.npy` para reducir costo y latencia). A diferencia de `EMB_PROVIDER=hash` (que asigna direcciones arbitrarias sin relación semántica), un modelo de embeddings entrenado coloca frases con significado similar cerca en el espacio vectorial.
3. **Normalización L2 y Similitud Coseno (`normalizar`, `coseno`):** Al normalizar cada fila (`axis=1`) a longitud unitaria ($\Vert{}v\Vert{}=1$), el coseno del ángulo entre la consulta $q$ y todos los fragmentos de la matriz $M$ se reduce a una sola multiplicación matricial rápida (`s = self.matriz @ q`), evitando que fragmentos más largos dominen por magnitud.
4. **Índice léxico vs. Índice denso (`Indice`):** El índice combina búsqueda por palabras clave (basada en coincidencia léxica de términos) y búsqueda vectorial densa (`buscar`), registrando cada ejecución en `bitacora/trazas.jsonl`.

---

## 5. Caso Aplicado (`v5-triage`) y Reflexión — [10 pts]
En la variante **`v5-triage` (Triage de incidentes)**, los ingenieros de guardia consultan runbooks (`rb-01` a `rb-08`) y postmortems (`pm-01` a `pm-03`) bajo presión durante caídas en producción:
- **¿Qué cambió al pasar de la guía común a `v5-triage`?** En `v5-triage` coexisten dos tipos de búsqueda muy marcados: descripciones coloquiales de síntomas (ej. `a01`: *"La base de datos ya no acepta más clientes y dice que se acabaron los lugares disponibles"*, donde el buscador vectorial acierta en `rb-03` y palabras clave falla) y búsquedas con códigos de error exactos de logs o IDs de runbooks (`QueuePool`, `OOMKilled`, `SSL: CERTIFICATE_VERIFY_FAILED`, `rb-04`, `pm-01`), donde las palabras clave aciertan con facilidad.
- **Reflexión sobre casos donde `acierto@1` falló (`a03` y `a05`):** En `a03` (lentitud en envíos interbancarios) y `a05` (errores 500 tras despliegue reciente), varios documentos del corpus comparten vocabulario muy cercano (por ejemplo, `rb-02` de latencia en transferencias, `rb-05` de proveedor SPEI, `rb-08` de reversa de despliegue y `pm-01` de postmortem tras despliegue). Aunque no quedaron en la posición 1 (`acierto@1 = 8/10`), **el buscador semántico logró `acierto@3 = 10/10`**, garantizando que el runbook correcto siempre entre en el contexto top-3 que recibirá el pipeline RAG en las siguientes entregas.

---

## 6. Evidencia y Bitácora de IA — [10 pts]
- **Bitácora de IA:** Documentada en `ai_log.md` detallando fecha, herramienta, prompts, qué se aceptó, qué se corrigió (retorno de objetos `Resultado` y limpieza de BOM en UTF-8) y validación con `pytest -q`.
- **Archivos de evidencia en repositorio:**
  - `bitacora/s1_comparacion.json` (comparación en `corpus/comun`).
  - `bitacora/a1_v5_comparacion.json` (comparación en `corpus/v5-triage`).
  - `evals/a1_v5-triage.jsonl` (10 casos de prueba de la variante `v5-triage`).
  - `bitacora/trazas.jsonl` (registro de llamadas y latencias).
'@ | Set-Content -Path "bitacora/reporte_a1.md" -Encoding UTF8