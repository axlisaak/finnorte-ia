---
id: ing-01
titulo: Revisión de código
clasificacion: interna
vigente: si
version: 2026-01
---
Todo cambio a la rama principal entra por pull request (PR). No se permite empujar directamente a main.

Número de aprobaciones: los PR que tocan movimiento de dinero, autenticación, autorización o datos personales requieren dos aprobaciones, y al menos una debe ser de una persona del equipo dueño del módulo. Los demás PR requieren una aprobación.

Tamaño: un PR no debe superar 400 líneas modificadas, sin contar archivos generados. Si el cambio es mayor, se divide en PR encadenados.

Tiempo de respuesta: la primera revisión debe ocurrir en máximo un día hábil. Si no ocurre, el autor puede escalar con la persona líder técnica del equipo.

La revisión verifica: que existan pruebas para el comportamiento nuevo, que no haya secretos en el código, que los errores se manejen y registren sin datos personales, y que la descripción del PR explique el porqué del cambio.

Los PR con código generado o asistido por IA deben indicarlo en la descripción con la etiqueta "asistido-por-ia". La persona autora es responsable del código como si lo hubiera escrito ella.
