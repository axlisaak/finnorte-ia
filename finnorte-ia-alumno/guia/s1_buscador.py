"""Guía S1 (viernes 16 oct) · Buscador semántico vs palabras clave sobre el Manual de Ingeniería.

    python guia/s1_buscador.py               # usa EMB_PROVIDER de tu .env
    EMB_PROVIDER=hash python guia/s1_buscador.py   # sin red (no entiende sinónimos: compáralo)

Qué hace
  1. Coseno a mano con 3 frases y vectores manuales (lo que pide la actividad oficial).
  2. Indexa corpus/comun y compara búsqueda semántica contra BM25 en 10 preguntas con respuesta conocida.
  3. Mide acierto@1 y acierto@3 de cada método y guarda bitacora/s1_comparacion.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from finnorte.config import config
from finnorte.retrieval import Indice, coseno, guardar_resultados, normalizar

print("── 1. Embeddings manuales (dimensiones: [seguridad, despliegue, pruebas, dinero]) ──")
frases = {
    "F1 Rotar las llaves de API cada 30 días": [0.9, 0.1, 0.0, 0.2],
    "F2 Revocar un secreto expuesto en el repositorio": [0.95, 0.05, 0.1, 0.1],
    "F3 Desplegar con canary los martes en la noche": [0.1, 0.9, 0.2, 0.3],
}
nombres, M = list(frases), np.array(list(frases.values()))
Mn = normalizar(M)
print("Normas tras normalizar:", np.round(np.linalg.norm(Mn, axis=1), 3))
print(f"cos(F1,F2) = {coseno(M[0], M[1]):.3f}   ← mismo tema (seguridad)")
print(f"cos(F1,F3) = {coseno(M[0], M[2]):.3f}   ← temas distintos")

print(f"\n── 2. Búsqueda en corpus/comun con embeddings '{config().emb_proveedor}' ──")
PRUEBAS = [
    ("¿Cada cuánto cambio las llaves de producción?", "ing-02"),
    ("subí una contraseña al repo por error", "ing-02"),
    ("¿cuántas personas tienen que aprobar mi PR de pagos?", "ing-01"),
    ("¿puedo liberar el día de quincena?", "ing-03"),
    ("se cayó transferencias para todos, ¿en cuánto respondo?", "ing-05"),
    ("¿cómo devuelvo los errores de mi servicio REST?", "ing-07"),
    ("¿puedo usar datos reales en el ambiente de QA?", "ing-04"),
    ("una librería tiene un CVE crítico", "ing-09"),
    ("necesito entrar a la base de datos productiva", "ing-10"),
    ("¿cuál es la meta de latencia de la API de transferencias?", "ing-12"),
]
ind = Indice.desde_carpeta("corpus/comun")
filas, ac = [], {"vector": [0, 0], "palabras": [0, 0]}
for q, esperado in PRUEBAS:
    v = [r.fragmento.doc_id for r in ind.buscar(q, k=3)]
    p = [r.fragmento.doc_id for r in ind.buscar_palabras(q, k=3)]
    for modo, lst in (("vector", v), ("palabras", p)):
        ac[modo][0] += lst[:1] == [esperado]
        ac[modo][1] += esperado in lst
    filas.append({"pregunta": q, "esperado": esperado, "vector": v, "palabras": p})
    print(f"{'✓' if v[:1] == [esperado] else '✗'} vec {'✓' if p[:1] == [esperado] else '✗'} pal  {q}")
n = len(PRUEBAS)
for modo, (a1, a3) in ac.items():
    print(f"{modo:9s} acierto@1 = {a1}/{n}   acierto@3 = {a3}/{n}")
print("Guardado en", guardar_resultados("s1_comparacion", filas))
