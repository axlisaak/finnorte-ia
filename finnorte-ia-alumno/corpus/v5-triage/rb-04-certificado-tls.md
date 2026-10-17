---
id: rb-04
titulo: Runbook: certificado TLS vencido o por vencer
clasificacion: interna
vigente: si
version: 2025-12
---
Síntoma en logs: "certificate has expired", "CERTIFICATE_VERIFY_FAILED" o "SSL: CERTIFICATE_VERIFY_FAILED" al conectar con un servicio interno o un proveedor.

Acciones: identificar el dominio en el error; si el certificado es nuestro, renovarlo con el gestor de certificados y reiniciar el balanceador; si es del proveedor, escalar a su soporte y activar la ruta alterna si existe.

Prevención: alerta 30 días antes del vencimiento. Ver postmortem pm-02.
