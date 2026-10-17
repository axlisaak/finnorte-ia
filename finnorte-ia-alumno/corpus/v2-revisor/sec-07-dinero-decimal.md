---
id: sec-07
titulo: Montos de dinero
clasificacion: interna
vigente: si
version: 2025-10
---
Regla SEC-07: los montos se representan con decimal.Decimal o en centavos enteros; nunca con float. Redondeo bancario (ROUND_HALF_EVEN) solo al final del cálculo.

Severidad: alta. Señal: operaciones de dinero con float(), round() sobre float o comparaciones de igualdad entre floats.
