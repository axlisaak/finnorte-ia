---
id: ing-03
titulo: Despliegues a producción
clasificacion: interna
vigente: si
version: 2026-03
---
Clasificación del riesgo del cambio: alto si toca dinero, autenticación, datos personales o el esquema de la base de datos de producción; medio si cambia una API pública o una dependencia; bajo en cualquier otro caso.

Ventanas: los cambios de riesgo alto se despliegan martes o jueves entre las 22:00 y las 02:00 (hora del centro de México). Los de riesgo medio y bajo, de lunes a jueves entre 10:00 y 17:00.

Congelamiento: no se despliega nada (salvo correcciones de incidentes de severidad 1 o 2) del 15 de diciembre al 6 de enero, ni los días 14, 15, 29, 30 y 31 de cada mes, porque concentran el pago de nómina.

Estrategia: riesgo alto usa despliegue gradual (canary) de 5 %, 50 % y 100 %, con al menos 30 minutos de observación entre etapas. Debe existir un plan de reversa probado en el ambiente de preproducción.

Aprobaciones: riesgo alto requiere aprobación de la persona líder técnica y de operaciones. Riesgo medio, de la persona líder técnica.
