---
id: ing-04
titulo: Clasificación de datos
clasificacion: publica
vigente: si
version: 2025-11
---
FinNorte clasifica la información en cuatro niveles:

Pública: puede compartirse fuera de la empresa (por ejemplo, tasas publicadas y comisiones vigentes).

Interna: para uso de personas colaboradoras (manuales, procesos, arquitectura general).

Confidencial: su divulgación causaría daño (umbrales antifraude, contratos con proveedores, resultados de auditorías).

Restringida: datos personales y financieros de clientes: nombre, correo, teléfono, CURP, RFC, CLABE, número de tarjeta, saldos y movimientos.

Reglas: los datos restringidos nunca se usan en ambientes de desarrollo o pruebas; se usan datos sintéticos. No se envían datos restringidos ni confidenciales a servicios externos que no estén aprobados por Seguridad, incluidos los asistentes de IA. Los registros (logs) no deben contener datos restringidos; se enmascaran antes de escribirse.
