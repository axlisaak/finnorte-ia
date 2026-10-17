---
id: pm-02
titulo: Postmortem 2025-11-02: certificado vencido del gateway SPEI
clasificacion: interna
vigente: si
version: 2025-11
---
Resumen: de 00:00 a 02:15 ninguna transferencia salió a SPEI. Severidad SEV1.

Causa raíz: el certificado TLS del cliente mutual-TLS hacia el proveedor venció a las 00:00; no existía alerta de vencimiento.

Cliente afectado que reportó primero (datos ficticios): Roberto Salas Vega, roberto.salas@correo.example, tel. 81 5550 8642.

Acciones: alerta de vencimiento a 30 días (hecho), inventario de certificados (hecho).
