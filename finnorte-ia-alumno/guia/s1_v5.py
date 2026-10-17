import json
from pathlib import Path
from finnorte.retrieval import Indice, guardar_resultados

ind = Indice.desde_carpeta("corpus/v5-triage")
casos = [json.loads(l) for l in Path("evals/a1_v5-triage.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]

filas, ac = [], {"vector": [0, 0], "palabras": [0, 0]}
for c in casos:
    q = c["entrada"]["pregunta"]
    esp = c["esperado"]["fuentes"][0]
    v = [r.fragmento.doc_id for r in ind.buscar(q, k=3)]
    p = [r.fragmento.doc_id for r in ind.buscar_palabras(q, k=3)]
    ac["vector"][0] += (v[:1] == [esp])
    ac["vector"][1] += (esp in v)
    ac["palabras"][0] += (p[:1] == [esp])
    ac["palabras"][1] += (esp in p)
    filas.append({"id": c["id"], "pregunta": q, "esperado": esp, "vector": v, "palabras": p})
    print(f"{'✓' if v[:1]==[esp] else '✗'} vec  {'✓' if p[:1]==[esp] else '✗'} pal  [{c['id']}] {q}")

n = len(casos)
for modo, (a1, a3) in ac.items():
    print(f"{modo:9s} acierto@1 = {a1}/{n}   acierto@3 = {a3}/{n}")
print("Guardado en", guardar_resultados("a1_v5_comparacion", filas))
