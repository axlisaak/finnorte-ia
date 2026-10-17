# FinNorte IA · Andamio del curso LSCA2318

Repositorio base del proyecto del curso **IA generativa aplicada a ingeniería de software**. FinNorte es una fintech ficticia; todos los datos son inventados.

Tu equipo construye, semana a semana, una herramienta de ingeniería que usa un LLM como componente. La herramienta debe medirse, resistir ataques y estar lista para tu portafolio.

> El andamio resuelve la plomería: llamar al modelo con cualquier proveedor, embeddings, bitácora, carga de prompts, evaluación y CI.
> Lo que se aprende lo construyes tú. Los `TODO` y las funciones con `NotImplementedError` son tu trabajo; las pruebas que les corresponden aparecen como *SKIP* hasta que las implementes.

## 1. Arranque (15 minutos)

```bash
git clone <tu-repo> && cd finnorte-ia
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt && pip install -e .
cp .env.example .env                                    # y pega tu llave
python -m finnorte info                                 # qué proveedor y modelo estás usando
python -m finnorte probar                               # una llamada real: verifica tu llave
pytest -q                                               # todo en verde o SKIP
```

**Llave gratuita:** en Google AI Studio (aistudio.google.com) → *Get API key*. Pégala en `.env` como `GEMINI_API_KEY`.

Alternativas:
- **Groq:** `LLM_PROVIDER=groq` y `GROQ_API_KEY`.
- **Ollama local, sin llave:** `LLM_PROVIDER=ollama` y `EMB_PROVIDER=ollama`.

Sin red, usa `LLM_PROVIDER=fake` y `EMB_PROVIDER=hash`. Es lo que usan las pruebas y el CI.

**Nunca subas `.env` al repositorio** (ya está en `.gitignore`). Si una llave se filtra, revócala en menos de 1 hora: es la política `ing-02` de FinNorte y también tu responsabilidad.

## 2. Estructura

| Carpeta / archivo | Qué es |
|---|---|
| `src/finnorte/llm.py` | `generar(prompt, sistema, json=True)`: misma interfaz para Gemini, Groq, Ollama y fake; reintentos con espera exponencial, costo y latencia |
| `src/finnorte/embeddings.py` | `embed(textos)` multi-proveedor |
| `src/finnorte/retrieval.py` | Corpus → fragmentos → índice vectorial y BM25. **A1:** `normalizar`, `coseno`, `buscar` |
| `src/finnorte/prompts.py` | Prompts versionados en `prompts/<id>.v<N>.md` |
| `src/finnorte/pipeline.py` | Flujos encadenados con validación de esquema. **A2:** `Pipeline.ejecutar` |
| `src/finnorte/controles.py` | Citas, abstención, clasificación, saneo de salida, autocrítica (Avance 1 y Avance 2) |
| `src/finnorte/pii.py` | Detección y enmascaramiento de datos personales (Avance 2) |
| `src/finnorte/herramientas.py` | Agente que propone acciones; el código las valida y ejecuta. **A4** |
| `src/finnorte/evaluacion.py` | Casos, métricas, contrato de calidad, LLM como juez, bootstrap |
| `src/finnorte/asistente.py` | **Caso guía** de los viernes: «Pregúntale al Manual de Ingeniería» |
| `src/finnorte/variante.py` | **Tu sistema**: el motor de la variante de tu equipo |
| `api/main.py`, `app/streamlit_app.py` | Servicio (S4) e interfaz (S5) del caso guía |
| `corpus/comun/` | Manual de Ingeniería (caso guía) |
| `corpus/<variante>/` | Corpus de tu variante (no lo modifiques sin documentarlo) |
| `datos/<variante>/` | Entradas de ejemplo de tu variante (requisitos, código, servicios, logs) |
| `evals/` | Casos de evaluación públicos. El profesor guarda un set oculto para la presentación |
| `contrato_calidad.yaml` | Metas medibles de tu equipo (se fijan en el Avance 1) |
| `ai_log.md` | Bitácora de uso de IA (obligatoria en todas las entregas) |
| `bitacora/` | Trazas JSONL de cada llamada, búsqueda, etapa y evaluación (evidencia) |
| `guia/` | Scripts de los laboratorios de los viernes |
| `.github/workflows/ci.yml` | Pruebas y evaluación contra el contrato en cada push |

## 3. Las 5 variantes

| Variante | Entrada | Salida | Herramienta del agente (A4) |
|---|---|---|---|
| `v1-qa` · Requisitos → pruebas | Requisito funcional | Casos Given/When/Then + pytest | Ejecutar pytest |
| `v2-revisor` · Revisor de código | Archivo Python | Hallazgos con regla SEC-xx + parche | Linter (ruff/bandit) |
| `v3-soporte` · Soporte a desarrolladores | Pregunta técnica | Respuesta citada + ejemplo | Consultar el esquema OpenAPI |
| `v4-documentador` · Documentador de APIs | Código de un servicio | README + OpenAPI | Validar la especificación |
| `v5-triage` · Triage de incidentes | Logs | Severidad, causa probable, acciones y borrador de postmortem | Buscar en logs por rango |

Detalle de cada una en [`VARIANTES.md`](VARIANTES.md).

## 4. Ruta del semestre (qué se enciende cada semana)

| Semana | Construyes | Entrega | Pruebas que se encienden |
|---|---|---|---|
| 1 | Buscador semántico de tu corpus | A1 | `test_a1_*` |
| 2 | Flujo de 4 etapas de tu variante | A2 | `test_a2_*` |
| 3 | Motor: RAG + controles + evaluación + contrato | **Avance 1** | `test_av1_*` |
| 4 | Servicio FastAPI con autenticación | A3 | tus pruebas de API |
| 5 | Interfaz + agente con una herramienta | A4 | `test_a4_*` |
| 6 | PII, saneo, red team cruzado, CI con contrato | **Avance 2** + A5 | `test_av2_*` |
| 7 | Integración, reporte de calidad, README de portafolio | **Entrega final** | todo en verde |

## 5. Comandos útiles

```bash
python -m finnorte buscar "rotación de secretos" [--palabras]
python -m finnorte preguntar "¿Puedo desplegar el 30?" [--sin-rag] [--sin-controles] [--v 1]
python -m finnorte evaluar evals/comun.jsonl --rep 3 --contrato contrato_calidad.yaml --salida bitacora/eval.json
python -m finnorte evaluar evals/v3-soporte.jsonl --sistema finnorte.variante:sistema --contrato contrato_calidad.yaml
python -m finnorte trazas                       # llamadas, tokens, costo y latencia acumulados
uvicorn api.main:app --reload                   # S4
streamlit run app/streamlit_app.py              # S5
```

## 6. Reglas del proyecto

1. **Prompts como código:** nunca edites un prompt "en caliente". Crea `.v2.md`, explica el cambio en `cambios:` y mide la diferencia.
2. **Evidencia o no pasó:** cada afirmación del reporte se respalda con un archivo de `bitacora/` o con una prueba.
3. **Bitácora de IA honesta:** usar IA está permitido y esperado; ocultarlo no. Registra qué aceptaste, qué cambiaste y cómo lo validaste.
4. **Datos:** solo el corpus y las entradas del curso; nada de datos reales.
5. **Commits de todos:** la contribución individual se revisa en el historial de Git.
