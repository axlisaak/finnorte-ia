---
id: ing-08
titulo: Estrategia de pruebas
clasificacion: interna
vigente: si
version: 2026-01
---
Pirámide: pruebas unitarias para la lógica, de integración para cada adaptador (base de datos, colas, proveedores externos) y de contrato para cada API pública.

Cobertura mínima: 80 % de ramas en los módulos que mueven dinero o manejan autenticación; 60 % en el resto. La cobertura no sustituye a la revisión de casos límite.

Datos de prueba: siempre sintéticos. Está prohibido copiar datos de producción a pruebas, aunque se enmascaren a mano.

Casos obligatorios en módulos de dinero: monto cero, monto negativo, monto en el límite exacto, operación repetida con la misma llave de idempotencia y falla del proveedor externo.

Las pruebas corren en el pipeline de integración continua en cada push; si fallan, no se permite el merge. Las pruebas inestables (flaky) se corrigen o se eliminan en máximo 5 días hábiles; no se marcan como ignoradas indefinidamente.
