---
id: sec-02
titulo: Consultas SQL parametrizadas
clasificacion: interna
vigente: si
version: 2025-12
---
Regla SEC-02: toda consulta SQL con datos externos usa parámetros (cursor.execute(sql, params)). Está prohibido construir SQL concatenando cadenas, con f-strings, con % o con .format().

Riesgo: inyección SQL (lectura o borrado de datos de otros clientes).

Severidad: crítica. Corrección: placeholders (%s, ?, :nombre) o el ORM; validar además el tipo de dato.
