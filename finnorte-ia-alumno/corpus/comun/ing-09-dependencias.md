---
id: ing-09
titulo: Gestión de dependencias
clasificacion: interna
vigente: si
version: 2025-10
---
Toda dependencia nueva requiere revisar su licencia, su mantenimiento (último release en los últimos 12 meses) y sus vulnerabilidades conocidas.

Licencias permitidas: MIT, BSD, Apache 2.0 e ISC. Las licencias GPL y AGPL requieren aprobación de Legal.

Análisis de composición (SCA): corre semanalmente y en cada PR que cambie el archivo de dependencias.

Plazos para corregir vulnerabilidades: críticas, 7 días naturales; altas, 30 días; medias, 90 días; bajas, en el siguiente ciclo de mantenimiento.

Las versiones se fijan (pin) en el archivo de dependencias; no se usan rangos abiertos en producción.
