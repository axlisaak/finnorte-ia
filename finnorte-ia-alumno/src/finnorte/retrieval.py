"""Recuperación: cargar el corpus, fragmentarlo, indexarlo con embeddings y buscar (T2, T6).

Formato de cada documento del corpus (Markdown con encabezado):

    ---
    id: pol-03
    titulo: Manejo de secretos
    clasificacion: interna        # publica | interna | confidencial
    vigente: si
    version: 2026-02
    ---
    Texto del documento…
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from . import trazas
from .config import RAIZ, config
from .embeddings import embed, tokens

STOP = set("""a al algo ante con contra de del desde donde el ella ellas ellos en entre era es esa ese eso esta este esto
estos fue ha hay la las le les lo los mas me mi mis muy no nos o para pero por que se si sin sobre su sus te tu un una
uno unos y ya como cual cuando cuanto debe deben puede puedo quiero tengo hace hacer ser son esta estan sea""".split())


@dataclass
class Documento:
    id: str
    titulo: str
    texto: str
    meta: dict = field(default_factory=dict)


@dataclass
class Fragmento:
    id: str            # "<doc_id>#<n>"
    doc_id: str
    titulo: str
    texto: str
    meta: dict = field(default_factory=dict)

    @property
    def clasificacion(self) -> str:
        return str(self.meta.get("clasificacion", "interna")).lower()


@dataclass
class Resultado:
    fragmento: Fragmento
    puntaje: float


# ───────────────────────────── corpus ─────────────────────────────
def leer_documento(ruta: Path) -> Documento:
    crudo = ruta.read_text(encoding="utf-8")
    meta: dict = {}
    cuerpo = crudo
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", crudo, re.S)
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea:
                k, v = linea.split(":", 1)
                meta[k.strip()] = v.split("#", 1)[0].strip()
        cuerpo = m.group(2)
    return Documento(id=meta.get("id", ruta.stem), titulo=meta.get("titulo", ruta.stem), texto=cuerpo.strip(), meta=meta)


def cargar_corpus(carpeta: str | Path = RAIZ / "corpus") -> list[Documento]:
    carpeta = Path(carpeta)
    return [leer_documento(p) for p in sorted(carpeta.rglob("*.md")) if not p.name.startswith("_")]


def fragmentar(doc: Documento, tam: int = 700, solape: int = 1) -> list[Fragmento]:
    """Parte el documento por párrafos hasta ~`tam` caracteres; repite `solape` párrafos entre fragmentos."""
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", doc.texto) if p.strip()]
    frags, actual = [], []
    for p in parrafos:
        if actual and sum(len(x) for x in actual) + len(p) > tam:
            frags.append(actual)
            actual = actual[-solape:] if solape else []
        actual.append(p)
    if actual:
        frags.append(actual)
    return [Fragmento(id=f"{doc.id}#{i}", doc_id=doc.id, titulo=doc.titulo, texto="\n\n".join(f), meta=doc.meta)
            for i, f in enumerate(frags)]


# ───────────────────────────── vectores (A1) ─────────────────────────────
def normalizar(m):
    n = np.linalg.norm(m, axis=1, keepdims=True)
    return m / np.where(n == 0, 1, n)


def coseno(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return 0.0 if na == 0 or nb == 0 else float(a @ b / (na * nb))


# ───────────────────────────── índice ─────────────────────────────
class Indice:
    """Índice vectorial en memoria con caché en disco (para no pagar embeddings dos veces)."""

    def __init__(self, fragmentos: list[Fragmento], proveedor: str | None = None):
        self.fragmentos = fragmentos
        self.proveedor = proveedor or config().emb_proveedor
        self.matriz = normalizar(self._embeddings_con_cache([f.texto for f in fragmentos]))
        self._bm25 = _BM25([f.texto for f in fragmentos])

    @classmethod
    def desde_carpeta(cls, carpeta: str | Path = RAIZ / "corpus", tam: int = 700, solape: int = 1,
                      proveedor: str | None = None) -> "Indice":
        frags = [f for d in cargar_corpus(carpeta) for f in fragmentar(d, tam, solape)]
        if not frags:
            raise ValueError(f"No hay documentos .md en {carpeta}")
        return cls(frags, proveedor)

    def _embeddings_con_cache(self, textos: list[str]) -> np.ndarray:
        clave = hashlib.sha1((self.proveedor + config().emb_modelo + "\x00".join(textos)).encode()).hexdigest()[:16]
        ruta = config().dir_trazas / f"emb_{clave}.npy"
        if ruta.exists():
            return np.load(ruta)
        m = embed(textos, self.proveedor)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        np.save(ruta, m)
        return m

    def buscar(self, consulta, k=3):
        q = normalizar(embed([consulta]))[0]
        s = self.matriz @ q
        orden = np.argsort(-s)[:k]
        return [Resultado(self.fragmentos[i], float(s[i])) for i in orden]

    def buscar_palabras(self, consulta: str, k: int = 4) -> list[Resultado]:
        """Línea base por palabras clave (BM25). Úsala para comparar contra la búsqueda semántica."""
        puntajes = self._bm25.puntajes(consulta)
        orden = sorted(range(len(puntajes)), key=lambda i: -puntajes[i])[:k]
        res = [Resultado(self.fragmentos[i], puntajes[i]) for i in orden if puntajes[i] > 0]
        trazas.registrar("busqueda", consulta=consulta[:200], k=k, modo="palabras",
                         resultados=[(r.fragmento.id, round(r.puntaje, 4)) for r in res])
        return res


class _BM25:
    def __init__(self, textos: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = [[t for t in tokens(x) if t not in STOP] for x in textos]
        self.k1, self.b = k1, b
        self.prom = sum(map(len, self.docs)) / max(1, len(self.docs))
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.tf = [Counter(d) for d in self.docs]

    def puntajes(self, consulta: str) -> list[float]:
        q = [t for t in tokens(consulta) if t not in STOP]
        out = []
        for d, tf in zip(self.docs, self.tf):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf.get(t, 0) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(d) / self.prom))
            out.append(s)
        return out


def contexto_para_prompt(resultados: list[Resultado], max_chars: int = 4000) -> str:
    """Formatea fragmentos como `[doc:ID] texto` para que el modelo pueda citarlos."""
    partes, total = [], 0
    for r in resultados:
        bloque = f"[doc:{r.fragmento.id}] {r.fragmento.titulo}\n{r.fragmento.texto}"
        if total + len(bloque) > max_chars:
            break
        partes.append(bloque)
        total += len(bloque)
    return "\n\n".join(partes)


def guardar_resultados(nombre: str, filas: list[dict]) -> Path:
    ruta = config().dir_trazas / f"{nombre}.json"
    ruta.write_text(json.dumps(filas, ensure_ascii=False, indent=2), encoding="utf-8")
    return ruta
