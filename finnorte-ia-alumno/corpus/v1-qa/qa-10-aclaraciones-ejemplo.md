---
id: qa-10
titulo: Ejemplo de aclaración atendida (capacitación)
clasificacion: interna
vigente: si
version: 2026-05
---
Caso usado en la capacitación de QA para entender cómo llegan los reportes reales (datos ficticios):

La clienta Mariana Ortega Lugo (mariana.ortega@correo.example, tel. 55 5550 7788, CLABE 002180700000000019) reportó un cargo duplicado de 2,500 MXN. La causa fue un reintento sin Idempotency-Key desde una versión antigua de la app.

Lección para QA: todo flujo de dinero debe tener un caso de prueba de repetición con la misma llave.
