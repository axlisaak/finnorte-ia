"""Prompts como código (T3): cada prompt es un archivo versionado en prompts/.

Nombre: prompts/<id>.v<N>.md   (p. ej. prompts/responder.v2.md)

    ---
    id: responder
    version: 2
    descripcion: Responde con citas a partir del contexto recuperado
    salida: json                      # json | texto
    esquema: respuesta.schema.json    # opcional, en prompts/esquemas/
    cambios: v2 agrega abstención cuando el contexto no alcanza
    ---
    ### SISTEMA
    Eres …
    ### USUARIO
    Contexto:
    {contexto}

    Pregunta: {pregunta}

Las variables van entre llaves. Para escribir una llave literal (p. ej. un ejemplo JSON) usa {{ y }}.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from .config import RAIZ

CARPETA = RAIZ / "prompts"


@dataclass
class Prompt:
    id: str
    version: int
    sistema: str
    usuario: str
    meta: dict = field(default_factory=dict)

    @property
    def variables(self) -> set[str]:
        limpio = (self.sistema + self.usuario).replace("{{", "").replace("}}", "")
        return set(re.findall(r"\{(\w+)\}", limpio))

    @property
    def salida_json(self) -> bool:
        return self.meta.get("salida", "texto").lower() == "json"

    @property
    def esquema(self) -> dict | None:
        nombre = self.meta.get("esquema")
        if not nombre:
            return None
        return json.loads((CARPETA / "esquemas" / nombre).read_text(encoding="utf-8"))

    def render(self, **valores) -> tuple[str, str]:
        faltan = self.variables - set(valores)
        if faltan:
            raise KeyError(f"Prompt {self.id}.v{self.version}: faltan variables {sorted(faltan)}")
        return self.sistema.format(**valores).strip(), self.usuario.format(**valores).strip()

    @property
    def nombre(self) -> str:
        return f"{self.id}.v{self.version}"


def _parsear(ruta: Path) -> Prompt:
    crudo = ruta.read_text(encoding="utf-8")
    meta: dict = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", crudo, re.S)
    cuerpo = crudo
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea:
                k, v = linea.split(":", 1)
                meta[k.strip()] = v.split("#", 1)[0].strip()
        cuerpo = m.group(2)
    partes = re.split(r"^###\s*(SISTEMA|USUARIO)\s*$", cuerpo, flags=re.M)
    secciones = {partes[i].upper(): partes[i + 1] for i in range(1, len(partes) - 1, 2)}
    vm = re.search(r"\.v(\d+)\.md$", ruta.name)
    return Prompt(id=meta.get("id", ruta.name.split(".")[0]), version=int(meta.get("version") or (vm.group(1) if vm else 1)),
                  sistema=secciones.get("SISTEMA", ""), usuario=secciones.get("USUARIO", cuerpo), meta=meta)


def versiones(id_: str) -> list[int]:
    return sorted(int(re.search(r"\.v(\d+)\.md$", p.name).group(1)) for p in CARPETA.glob(f"{id_}.v*.md"))


def cargar(id_: str, version: int | None = None) -> Prompt:
    """Carga un prompt por id; sin versión, la más reciente."""
    vs = versiones(id_)
    if not vs:
        raise FileNotFoundError(f"No existe prompts/{id_}.v*.md")
    v = version or vs[-1]
    ruta = CARPETA / f"{id_}.v{v}.md"
    if not ruta.exists():
        raise FileNotFoundError(f"No existe {ruta.name}; versiones disponibles: {vs}")
    return _parsear(ruta)
