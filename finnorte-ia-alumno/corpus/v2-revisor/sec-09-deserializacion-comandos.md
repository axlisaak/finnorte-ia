---
id: sec-09
titulo: Deserialización y comandos del sistema
clasificacion: interna
vigente: si
version: 2025-12
---
Regla SEC-09: no se usan pickle.loads, yaml.load sin SafeLoader ni eval/exec sobre datos externos. No se ejecutan comandos con shell=True ni os.system con datos externos; se usa subprocess con lista de argumentos.

Severidad: crítica.
