"""Adaptador multi-proveedor para LLM: una sola función, `generar`, sin importar el proveedor.

    from finnorte.llm import generar
    r = generar("Resume este texto…", sistema="Eres…", json=True)
    r.texto, r.datos (si json=True), r.tokens_entrada, r.costo_usd, r.latencia_ms

Proveedores: gemini, groq, ollama y fake (sin red: para pruebas, CI y clase sin internet).
Cambiar de proveedor = cambiar LLM_PROVIDER en .env. Tu lógica no se toca (patrón adaptador, T13).
"""
from __future__ import annotations

import json as _json
import random
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable

import requests

from . import trazas
from .config import PRECIOS, Config, config

ERRORES_REINTENTABLES = {408, 429, 500, 502, 503, 504}


class LLMError(RuntimeError):
    """Falla del proveedor que no se resolvió con reintentos."""


@dataclass
class Respuesta:
    texto: str
    proveedor: str
    modelo: str
    tokens_entrada: int = 0
    tokens_salida: int = 0
    latencia_ms: float = 0.0
    intentos: int = 1
    datos: Any = None          # JSON ya interpretado cuando se pidió json=True
    extra: dict = field(default_factory=dict)

    @property
    def costo_usd(self) -> float:
        pin, pout = PRECIOS.get(self.proveedor, (0.0, 0.0))
        return (self.tokens_entrada * pin + self.tokens_salida * pout) / 1_000_000


# ───────────────────────────── utilidades ─────────────────────────────
def extraer_json(texto: str) -> Any:
    """Interpreta JSON aunque venga envuelto en ```json … ``` o con texto alrededor."""
    t = texto.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if m:
        t = m.group(1).strip()
    try:
        return _json.loads(t)
    except _json.JSONDecodeError:
        ini = min([i for i in (t.find("{"), t.find("[")) if i >= 0], default=-1)
        fin = max(t.rfind("}"), t.rfind("]"))
        if ini >= 0 and fin > ini:
            return _json.loads(t[ini:fin + 1])
        raise


def _estimar_tokens(texto: str) -> int:
    return max(1, len(texto) // 4)


def _post(url: str, cfg: Config, **kw) -> tuple[dict, int]:
    """POST con reintentos y espera exponencial con jitter (T9)."""
    ultimo = None
    for intento in range(1, cfg.reintentos + 2):
        try:
            r = requests.post(url, timeout=cfg.timeout_s, **kw)
            if r.status_code in ERRORES_REINTENTABLES:
                ultimo = LLMError(f"HTTP {r.status_code}: {r.text[:200]}")
            elif r.status_code >= 400:
                raise LLMError(f"HTTP {r.status_code}: {r.text[:300]}")
            else:
                return r.json(), intento
        except requests.RequestException as e:
            ultimo = LLMError(f"Red: {e}")
        if intento <= cfg.reintentos:
            time.sleep((2 ** (intento - 1)) + random.random() * 0.3)
    raise ultimo or LLMError("Falla desconocida")


# ───────────────────────────── proveedores ─────────────────────────────
def _gemini(prompt, sistema, historial, json, temperatura, cfg: Config):
    if not cfg.gemini_key:
        raise LLMError("Falta GEMINI_API_KEY en .env")
    contents = [{"role": "model" if h["rol"] != "user" else "user", "parts": [{"text": h["texto"]}]} for h in historial]
    contents.append({"role": "user", "parts": [{"text": prompt}]})
    body: dict = {"contents": contents, "generationConfig": {"temperature": temperatura}}
    if sistema:
        body["systemInstruction"] = {"parts": [{"text": sistema}]}
    if json:
        body["generationConfig"]["responseMimeType"] = "application/json"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{cfg.llm_modelo}:generateContent"
    d, intentos = _post(url, cfg, json=body, headers={"x-goog-api-key": cfg.gemini_key})
    try:
        texto = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    except (KeyError, IndexError):
        motivo = d.get("promptFeedback", {}).get("blockReason") or d.get("candidates", [{}])[0].get("finishReason")
        raise LLMError(f"Respuesta vacía o bloqueada ({motivo})")
    u = d.get("usageMetadata", {})
    return texto, u.get("promptTokenCount", 0), u.get("candidatesTokenCount", 0), intentos


def _groq(prompt, sistema, historial, json, temperatura, cfg: Config):
    if not cfg.groq_key:
        raise LLMError("Falta GROQ_API_KEY en .env")
    msgs = ([{"role": "system", "content": sistema}] if sistema else [])
    msgs += [{"role": "assistant" if h["rol"] != "user" else "user", "content": h["texto"]} for h in historial]
    msgs.append({"role": "user", "content": prompt})
    body: dict = {"model": cfg.llm_modelo, "messages": msgs, "temperature": temperatura}
    if json:
        body["response_format"] = {"type": "json_object"}
    d, intentos = _post("https://api.groq.com/openai/v1/chat/completions", cfg, json=body,
                        headers={"Authorization": f"Bearer {cfg.groq_key}"})
    u = d.get("usage", {})
    return d["choices"][0]["message"]["content"], u.get("prompt_tokens", 0), u.get("completion_tokens", 0), intentos


def _ollama(prompt, sistema, historial, json, temperatura, cfg: Config):
    msgs = ([{"role": "system", "content": sistema}] if sistema else [])
    msgs += [{"role": "assistant" if h["rol"] != "user" else "user", "content": h["texto"]} for h in historial]
    msgs.append({"role": "user", "content": prompt})
    body: dict = {"model": cfg.llm_modelo, "messages": msgs, "stream": False, "options": {"temperature": temperatura}}
    if json:
        body["format"] = "json"
    d, intentos = _post(f"{cfg.ollama_url}/api/chat", cfg, json=body)
    return d["message"]["content"], d.get("prompt_eval_count", 0), d.get("eval_count", 0), intentos


class _Fake:
    """Proveedor simulado y determinista.

    Por defecto: si se pide JSON, responde con el primer fragmento citado en el prompt
    (marcas [doc:ID]) para que un flujo RAG funcione de punta a punta sin red.
    En pruebas puedes reemplazar el comportamiento:  llm.fake.responder = lambda prompt, sistema: "..."
    """

    responder: Callable[[str, str], str] | None = None

    def __call__(self, prompt, sistema, historial, json, temperatura, cfg):
        if self.responder:
            texto = self.responder(prompt, sistema or "")
        elif json:
            ids = re.findall(r"\[doc:([\w\-./#]+)\]", prompt)
            frag = ""
            if ids:
                m = re.search(r"\[doc:" + re.escape(ids[0]) + r"\]\s*(.+)", prompt)
                frag = (m.group(1) if m else "")[:220]
            texto = _json.dumps({
                "respuesta": frag or "No encontré información suficiente en el contexto.",
                "fuentes": ids[:2],
                "abstuvo": not ids,
                "confianza": 0.7 if ids else 0.2,
            }, ensure_ascii=False)
        else:
            ultima = [l for l in prompt.strip().splitlines() if l.strip()][-1:] or [""]
            texto = f"[respuesta simulada] {ultima[0][:200]}"
        return texto, _estimar_tokens((sistema or "") + prompt), _estimar_tokens(texto), 1


fake = _Fake()
_PROVEEDORES = {"gemini": _gemini, "groq": _groq, "ollama": _ollama, "fake": fake}


# ───────────────────────────── API pública ─────────────────────────────
def generar(prompt: str, sistema: str | None = None, *, json: bool = False, temperatura: float = 0.2,
            historial: list[dict] | None = None, proveedor: str | None = None, modelo: str | None = None,
            etiqueta: str = "", registrar: bool = True) -> Respuesta:
    """Llama al modelo configurado y devuelve una `Respuesta` uniforme.

    historial: lista de {"rol": "user"|"model", "texto": "..."} (memoria de conversación, T9).
    etiqueta: nombre de la etapa o del experimento; aparece en la bitácora.
    """
    cfg = config()
    if proveedor:
        cfg.llm_proveedor = proveedor
        cfg.llm_modelo = modelo or ""
        cfg.__post_init__()
    elif modelo:
        cfg.llm_modelo = modelo
    fn = _PROVEEDORES.get(cfg.llm_proveedor)
    if fn is None:
        raise LLMError(f"Proveedor desconocido: {cfg.llm_proveedor}")
    t0 = time.perf_counter()
    error = None
    try:
        texto, tin, tout, intentos = fn(prompt, sistema, historial or [], json, temperatura, cfg)
    except LLMError as e:
        error = str(e)
        if registrar:
            trazas.registrar("llm", etiqueta=etiqueta, proveedor=cfg.llm_proveedor, modelo=cfg.llm_modelo,
                             ok=False, error=error, latencia_ms=round((time.perf_counter() - t0) * 1000, 1))
        raise
    r = Respuesta(texto=texto, proveedor=cfg.llm_proveedor, modelo=cfg.llm_modelo, tokens_entrada=tin,
                  tokens_salida=tout, latencia_ms=round((time.perf_counter() - t0) * 1000, 1), intentos=intentos)
    if json:
        try:
            r.datos = extraer_json(texto)
        except ValueError:
            r.datos = None
    if registrar:
        trazas.registrar("llm", etiqueta=etiqueta, proveedor=r.proveedor, modelo=r.modelo, ok=True,
                         tokens_entrada=r.tokens_entrada, tokens_salida=r.tokens_salida, intentos=r.intentos,
                         latencia_ms=r.latencia_ms, costo_usd=round(r.costo_usd, 6), json_valido=(r.datos is not None) if json else None)
    return r
