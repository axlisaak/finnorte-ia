---
id: qa-08
titulo: Guía de casos de prueba de FinNorte
clasificacion: interna
vigente: si
version: 2026-04
---
Formato: Gherkin en español (Dado / Cuando / Entonces). Un escenario prueba una sola conducta.

Nombre: CP-<requisito>-<número>, por ejemplo CP-RF07-03. Cada escenario lleva la etiqueta del requisito (@RF07) para trazabilidad.

Tipos obligatorios por requisito: al menos un caso positivo, uno negativo y uno de límite. En operaciones de dinero, además: monto cero, monto negativo, valor exactamente en el límite, un centavo arriba del límite y repetición con la misma Idempotency-Key.

El "Entonces" debe ser verificable: un valor, un mensaje exacto o un estado. Si el requisito no dice cuál es el resultado esperado, el caso se marca SUPUESTO y se pregunta al dueño del producto; no se inventa.

Datos: siempre sintéticos. No se usan nombres, correos ni CLABE de clientes reales.
