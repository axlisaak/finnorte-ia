---
id: doc-05
titulo: Qué no se documenta en documentos públicos o de socios
clasificacion: interna
vigente: si
version: 2026-04
---
No se publica en documentación para socios ni en READMEs de repositorios compartidos:
- Endpoints bajo /internal/ o /admin/.
- Valores de secretos, llaves o tokens (aunque estén en el código por error: se reporta como hallazgo de seguridad, no se copian).
- Nombres de tablas, servidores o direcciones IP internas.
- Datos reales de clientes o de personas colaboradoras.

Si el código contiene un secreto, la documentación lo menciona como variable de entorno (por ejemplo PAGOS_API_KEY) y se abre un reporte a Seguridad.
