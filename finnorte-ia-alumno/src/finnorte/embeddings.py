"""Embeddings multi-proveedor: `embed(textos) -> np.ndarray` de forma (n, d).

Proveedores
- gemini : gemini-embedding-001 por API (requiere GEMINI_API_KEY)
- ollama : nomic-embed-text en tu equipo (ollama pull nomic-embed-text)
- local  : sentence-transformers (pip install sentence-transformers); corre en CPU o Colab
- hash   : sin red ni modelo. Cuenta palabras y trigramas de letras en 512 casillas.
           Sirve para pruebas y CI; NO captura sinónimos (compáralo contra un modelo real en A1).
"""
from __future__ import annotations

import hashlib
import re
import unicodedata
from functools import lru_cache

import numpy as np
import requests

from .config import config


def _sin_acentos(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


def tokens(texto: str) -> list[str]:
    return re.findall(r"[a-z0-9ñ]+", _sin_acentos(texto))


def _hash(textos: list[str], dim: int = 512) -> np.ndarray:
    m = np.zeros((len(textos), dim), dtype=np.float32)
    for i, t in enumerate(textos):
        ws = tokens(t)
        feats = ws + [w[j:j + 3] for w in ws if len(w) > 3 for j in range(len(w) - 2)]
        for f in feats:
            h = int(hashlib.md5(f.encode()).hexdigest(), 16)
            m[i, h % dim] += 1.0 if (h >> 9) & 1 else -1.0
    return m


def _gemini(textos: list[str]) -> np.ndarray:
    cfg = config()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{cfg.emb_modelo}:batchEmbedContents"
    salida = []
    for i in range(0, len(textos), 100):
        lote = textos[i:i + 100]
        body = {"requests": [{"model": f"models/{cfg.emb_modelo}", "content": {"parts": [{"text": t}]}} for t in lote]}
        r = requests.post(url, json=body, headers={"x-goog-api-key": cfg.gemini_key}, timeout=cfg.timeout_s)
        r.raise_for_status()
        salida += [e["values"] for e in r.json()["embeddings"]]
    return np.array(salida, dtype=np.float32)


def _ollama(textos: list[str]) -> np.ndarray:
    cfg = config()
    r = requests.post(f"{cfg.ollama_url}/api/embed", json={"model": cfg.emb_modelo, "input": textos}, timeout=cfg.timeout_s)
    r.raise_for_status()
    return np.array(r.json()["embeddings"], dtype=np.float32)


@lru_cache(maxsize=1)
def _modelo_local(nombre: str):
    from sentence_transformers import SentenceTransformer  # importación perezosa: es pesada
    return SentenceTransformer(nombre)


def _local(textos: list[str]) -> np.ndarray:
    return np.asarray(_modelo_local(config().emb_modelo).encode(textos), dtype=np.float32)


_PROV = {"hash": _hash, "gemini": _gemini, "ollama": _ollama, "local": _local}


def embed(textos: list[str] | str, proveedor: str | None = None) -> np.ndarray:
    """Devuelve una matriz (n, d) SIN normalizar. Normalizar es tarea tuya (A1)."""
    if isinstance(textos, str):
        textos = [textos]
    p = (proveedor or config().emb_proveedor).lower()
    if p not in _PROV:
        raise ValueError(f"Proveedor de embeddings desconocido: {p}")
    return _PROV[p](list(textos))
