---
id: api-05
titulo: Webhooks
clasificacion: publica
vigente: si
version: 2026-02
---
FinNorte envía eventos (transferencia.liquidada, transferencia.rechazada, transferencia.devuelta) por POST a la URL registrada por el socio.

Firma: cada evento incluye el encabezado X-FinNorte-Signature con el HMAC-SHA256 del cuerpo usando el secreto del webhook. El socio debe verificar la firma antes de procesar y rechazar eventos con más de 5 minutos de antigüedad (campo timestamp).

Respuesta: el socio debe responder 2xx en máximo 10 segundos. Si no, FinNorte reintenta 5 veces con espera exponencial (1, 2, 4, 8 y 16 minutos).

Los eventos pueden llegar duplicados o fuera de orden: se deduplican con el campo evento_id.
