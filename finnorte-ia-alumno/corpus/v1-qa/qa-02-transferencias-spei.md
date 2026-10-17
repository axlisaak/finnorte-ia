---
id: qa-02
titulo: Transferencias SPEI
clasificacion: interna
vigente: si
version: 2026-03
---
Monto mínimo por transferencia: 1.00 MXN. Montos con más de dos decimales se rechazan.

Monto máximo por operación: 8,000 MXN para cuentas nivel 1 y 50,000 MXN para cuentas nivel 2. Un monto igual al máximo se acepta; un centavo más se rechaza con el mensaje "El monto excede el límite por operación".

CLABE destino: 18 dígitos con dígito verificador válido. Una CLABE inválida se rechaza antes de llamar a SPEI.

Concepto: obligatorio, máximo 40 caracteres, sin caracteres especiales fuera de letras, números y espacios.

Las transferencias operan 24/7. Toda transferencia requiere confirmación con el segundo factor (código de 6 dígitos) y lleva Idempotency-Key: repetir la solicitud con la misma llave en 24 horas no genera un segundo cargo.
