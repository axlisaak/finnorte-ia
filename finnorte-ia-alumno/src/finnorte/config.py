"""Configuración central. Todo se lee de variables de entorno (archivo .env).

Variables principales
---------------------
LLM_PROVIDER   gemini | groq | ollama | fake      (por defecto: gemini si hay GEMINI_API_KEY, si no fake)
LLM_MODEL      nombre del modelo del proveedor     (hay uno por defecto para cada proveedor)
EMB_PROVIDER   gemini | ollama | local | hash      (hash = sin red, para pruebas y CI)
GEMINI_API_KEY, GROQ_API_KEY, OLLAMA_URL
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]


def _cargar_env(archivo: Path = RAIZ / ".env") -> None:
    """Lector mínimo de .env (sin dependencias). No sobrescribe variables ya definidas."""
    if not archivo.exists():
        return
    for linea in archivo.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip('"').strip("'"))


_cargar_env()

MODELOS_POR_DEFECTO = {
    "gemini": "gemini-2.5-flash",
    "groq": "llama-3.3-70b-versatile",
    "ollama": "llama3.2",
    "fake": "fake-1",
}
EMB_POR_DEFECTO = {
    "gemini": "gemini-embedding-001",
    "ollama": "nomic-embed-text",
    "local": "paraphrase-multilingual-MiniLM-L12-v2",
    "hash": "hash-512",
}

# Precios ILUSTRATIVOS en US$ por millón de tokens (entrada, salida).
# Verifica la página de precios vigente de tu proveedor y actualiza esta tabla:
# es la base del cálculo de costo de tu contrato de calidad.
PRECIOS = {
    "gemini": (0.30, 2.50),
    "groq": (0.59, 0.79),
    "ollama": (0.0, 0.0),
    "fake": (0.0, 0.0),
}


def _proveedor_llm() -> str:
    p = os.getenv("LLM_PROVIDER")
    if p:
        return p.lower()
    return "gemini" if os.getenv("GEMINI_API_KEY") else "fake"


def _proveedor_emb() -> str:
    p = os.getenv("EMB_PROVIDER")
    if p:
        return p.lower()
    return "gemini" if os.getenv("GEMINI_API_KEY") else "hash"


@dataclass
class Config:
    llm_proveedor: str = field(default_factory=_proveedor_llm)
    llm_modelo: str = ""
    emb_proveedor: str = field(default_factory=_proveedor_emb)
    emb_modelo: str = ""
    gemini_key: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))
    groq_key: str = field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    ollama_url: str = field(default_factory=lambda: os.getenv("OLLAMA_URL", "http://localhost:11434"))
    timeout_s: float = float(os.getenv("LLM_TIMEOUT", "60"))
    reintentos: int = int(os.getenv("LLM_RETRIES", "3"))
    dir_trazas: Path = RAIZ / "bitacora"

    def __post_init__(self) -> None:
        self.llm_modelo = self.llm_modelo or os.getenv("LLM_MODEL") or MODELOS_POR_DEFECTO.get(self.llm_proveedor, "")
        self.emb_modelo = self.emb_modelo or os.getenv("EMB_MODEL") or EMB_POR_DEFECTO.get(self.emb_proveedor, "")


def config() -> Config:
    return Config()
