---
id: api-10
titulo: Datos de prueba del sandbox
clasificacion: publica
vigente: si
version: 2026-03
---
En sandbox, el resultado de una transferencia depende de los centavos del monto:
- termina en 00: se liquida.
- termina en 01: se rechaza por fondos insuficientes (FN-4002).
- termina en 02: se liquida y después se devuelve.
- termina en 03: SPEI no disponible (FN-5031).

Las CLABE de prueba válidas comienzan con 646180 (banco ficticio de pruebas).
