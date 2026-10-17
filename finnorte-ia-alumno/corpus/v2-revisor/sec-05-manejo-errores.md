---
id: sec-05
titulo: Manejo de errores
clasificacion: interna
vigente: si
version: 2025-11
---
Regla SEC-05: no se capturan excepciones con except: o except Exception: para ignorarlas en silencio. Las excepciones se registran y se traducen a una respuesta problem+json sin trazas de pila ni detalles internos.

Severidad: media. Excepción: un except amplio en el punto de entrada del servicio, siempre que registre y responda un error genérico.
