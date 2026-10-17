"""finnorte — andamio del curso LSCA2318 (IA generativa aplicada a ingeniería de software).

Módulos
- llm           adaptador multi-proveedor (gemini, groq, ollama, fake)
- embeddings    embeddings multi-proveedor (gemini, ollama, local, hash)
- retrieval     corpus, fragmentos, índice vectorial y BM25
- prompts       prompts versionados en archivos
- pipeline      flujos encadenados con validación de esquema
- controles     citas, abstención, clasificación, saneo de salida, autocrítica
- pii           detección y enmascaramiento de datos personales
- evaluacion    casos, métricas, contrato de calidad, LLM como juez, bootstrap
- herramientas  agente que propone acciones; el código decide y ejecuta
- trazas        bitácora JSONL de todo lo anterior
- asistente     caso guía de los viernes (Manual de Ingeniería de FinNorte)
"""
__version__ = "1.0.0"
