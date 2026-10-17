# Las 5 variantes del proyecto

Todas comparten el mismo esqueleto y se califican con la misma rúbrica. Lo que cambia es el dominio, la entrada, el artefacto y los controles específicos.

Cada variante trae una trampa propia en su corpus:
- datos personales ficticios;
- un documento `confidencial`;
- en algunas, una versión obsoleta o una "excepción" que no debe filtrarse.

Encontrarlas y defenderlas es parte del reto.

---

## v1-qa · Requisitos → pruebas
**Usuario:** QA y desarrolladores de FinNorte.
**Problema:** escribir casos de prueba completos (positivos, negativos, límite, idempotencia) toma horas y se omiten los bordes.

- **Entrada:** un requisito funcional (`datos/v1-qa/requisitos/`).
- **Corpus:** reglas de negocio (registro, SPEI, límites, comisiones, tarjetas, sesiones, niveles) y la guía de casos de prueba de FinNorte (`qa-08`).
- **Artefacto:** JSON con casos `CP-RFxx-nn`, etiqueta `@RFxx`, tipo y Dado/Cuando/Entonces con valores exactos tomados del corpus. Después se exportan a un archivo pytest ejecutable.
- **Etapas sugeridas:** analizar requisito → recuperar reglas → generar casos → revisar cobertura contra `qa-08` → exportar pytest.
- **Controles propios:**
  - todo "Entonces" cita la regla de la que sale;
  - lo que el corpus no dice se marca `SUPUESTO`;
  - el pytest generado compila (`ast.parse`).
- **Herramienta del agente:** ejecutar pytest sobre los casos generados y leer el resultado.
- **Trampa:** `qa-10` trae datos de una clienta. Nunca deben aparecer como datos de prueba.

## v2-revisor · Revisor de código con políticas internas
**Usuario:** quien revisa pull requests.
**Problema:** las revisiones omiten reglas internas (SEC-01 a SEC-10) y los revisores automáticos genéricos no conocen las de FinNorte.

- **Entrada:** archivo Python (`datos/v2-revisor/codigo/`) o un diff.
- **Corpus:** guía de código seguro (SEC-01 a SEC-10).
- **Artefacto:** JSON con hallazgos `{regla, linea, severidad, explicacion, parche}`, o `"sin hallazgos"` si el código está limpio.
- **Etapas sugeridas:** detectar patrones (código) → recuperar reglas → explicar hallazgos → proponer parche → verificar que el parche no rompa (compila).
- **Controles propios:**
  - cada hallazgo cita una regla que existe;
  - la línea reportada existe en el archivo;
  - en código limpio (`limites.py`), cero falsos positivos.
- **Herramienta del agente:** correr `ruff` o `bandit` y contrastar con sus hallazgos.
- **Trampa:** `sec-11` es confidencial (excepciones con nombre y correo), y algunos archivos traen comentarios que intentan dar órdenes al revisor.

## v3-soporte · Soporte a desarrolladores de socios
**Usuario:** desarrolladores externos que integran la API de FinNorte.
**Problema:** las mismas preguntas llegan al soporte todos los días y las respuestas sin fuente generan integraciones rotas.

- **Entrada:** pregunta en lenguaje natural.
- **Corpus:** documentación de la API (autenticación, cuentas, transferencias, webhooks, errores, límites, deprecaciones, SDK, sandbox).
- **Artefacto:** respuesta de máximo 150 palabras con cita y, cuando aplique, un ejemplo (curl o Python) que use solo campos documentados.
- **Etapas sugeridas:** clasificar intención → recuperar → responder con cita → verificar que los endpoints y campos del ejemplo existen en el corpus.
- **Controles propios:**
  - abstención fuera de dominio;
  - avisar cuando un endpoint está deprecado (`api-08`);
  - nunca credenciales.
- **Herramienta del agente:** consultar un esquema OpenAPI (dado por el profesor en S5) para validar rutas y campos.
- **Trampa:** `api-11` es confidencial y contiene credenciales y datos de contacto.

## v4-documentador · Documentador de APIs
**Usuario:** equipos de desarrollo que deben publicar documentación.
**Problema:** la documentación se queda atrás del código o inventa comportamiento.

- **Entrada:** código de un servicio FastAPI (`datos/v4-documentador/servicios/`).
- **Corpus:** guía de estilo, plantilla README, reglas OpenAPI, convenciones, qué no documentar, errores, changelog, ejemplos sintéticos.
- **Artefacto:** README con las 8 secciones de `doc-02` y especificación OpenAPI 3.1 (JSON o YAML).
- **Etapas sugeridas:** extraer endpoints con `ast` (código, no modelo) → recuperar reglas → redactar README → generar OpenAPI → validar la especificación y comparar endpoints contra el código.
- **Controles propios:**
  - cada endpoint documentado existe en el código y cada `HTTPException` aparece en la documentación;
  - no se documentan rutas `/internal` ni `/admin`;
  - los secretos se mencionan solo como variable de entorno.
- **Herramienta del agente:** validador OpenAPI (`openapi-spec-validator`).
- **Trampa:** `pagos_api.py` trae una llave escrita en el código y un endpoint interno; `doc-09` es confidencial.

## v5-triage · Triage de incidentes
**Usuario:** la persona de guardia a las 3 a. m.
**Problema:** ante una alerta, encontrar el runbook correcto y decidir la severidad toma minutos críticos.

- **Entrada:** extracto de logs (`datos/v5-triage/logs/`).
- **Corpus:** catálogo de severidades, runbooks y postmortems anteriores.
- **Artefacto:** JSON con `{severidad, sintomas, causa_probable, runbook, acciones_inmediatas, incidentes_similares, borrador_postmortem}`.
- **Etapas sugeridas:** extraer señales del log (código: regex de errores, despliegues, métricas) → recuperar runbooks → clasificar severidad con `rb-01` → proponer acciones → buscar postmortems similares.
- **Controles propios:**
  - la severidad sigue la regla de `rb-01`;
  - toda acción proviene de un runbook citado;
  - nunca proponer "reiniciar todo";
  - enmascarar PII que aparezca en los logs.
- **Herramienta del agente:** buscar en los logs por rango de tiempo o patrón.
- **Trampa:** `pm-02` trae datos de un cliente; algunos logs incluyen correos y CLABE, o instrucciones para cambiar la severidad.
