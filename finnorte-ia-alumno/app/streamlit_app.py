"""Interfaz del caso guía (S5).  streamlit run app/streamlit_app.py

Dos modos:
- Preguntar: RAG con citas y abstención (motor del Avance 1).
- Agente: el modelo propone herramientas; las sensibles piden confirmación en pantalla.
Diseño (T9): estado de espera visible, errores con salida, fuentes desplegables, costo y latencia a la vista.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import streamlit as st

from finnorte import llm
from finnorte.asistente import Asistente
from finnorte.config import config
from finnorte.guia_herramientas import TICKETS, herramientas_guia
from finnorte.herramientas import ejecutar_agente

st.set_page_config(page_title="FinNorte · Manual de Ingeniería", page_icon="📘", layout="wide")


@st.cache_resource
def cargar():
    return Asistente.crear()


asis = cargar()
c = config()
st.sidebar.markdown(f"**Modelo:** {c.llm_proveedor}/{c.llm_modelo}  \n**Embeddings:** {c.emb_proveedor}")
modo = st.sidebar.radio("Modo", ["Preguntar", "Agente"])
st.sidebar.caption("Ficticio · uso educativo · LSCA2318")

st.title("📘 Manual de Ingeniería de FinNorte")

if modo == "Preguntar":
    st.caption("Respondo solo con el manual y cito la fuente. Si no está en el manual, te lo digo.")
    ejemplos = ["¿Cada cuánto se rotan los secretos de producción?", "¿Puedo desplegar el 30 de este mes?",
                "¿Qué formato tienen los errores de la API?"]
    cols = st.columns(len(ejemplos))
    for col, e in zip(cols, ejemplos):
        if col.button(e, use_container_width=True):
            st.session_state["pregunta"] = e
    pregunta = st.text_input("Tu pregunta", key="pregunta", max_chars=500)
    if st.button("Preguntar", type="primary", disabled=not pregunta.strip()):
        with st.spinner("Buscando en el manual y redactando…"):
            try:
                out = asis.responder(pregunta)
            except llm.LLMError as e:
                st.error("El modelo no respondió a tiempo. Intenta de nuevo o consulta el manual directamente.")
                st.caption(f"Detalle técnico: {str(e)[:160]}")
                st.stop()
        (st.warning if out["abstuvo"] else st.success)(out["respuesta"])
        if out["fuentes"]:
            with st.expander(f"Fuentes ({len(out['fuentes'])})"):
                for f in out["fuentes"]:
                    frag = next((x for x in asis.indice.fragmentos if x.id == f or x.doc_id == f), None)
                    st.markdown(f"**{f}** · {frag.titulo if frag else ''}")
                    if frag:
                        st.caption(frag.texto[:500])
        st.caption(f"⏱ {out['latencia_ms']:.0f} ms · 💲 US${out['costo_usd']:.5f} · recuperados: {out['recuperados']}")
else:
    st.caption("El agente puede buscar en el manual, revisar ventanas de despliegue y PROPONER crear un ticket. "
               "Crear el ticket requiere tu confirmación.")
    tarea = st.text_area("Tarea", "Quiero desplegar un cambio de riesgo alto en pagos-api el 2026-11-10. ¿Se puede? Si sí, crea el ticket.")
    confirmar_tickets = st.checkbox("Autorizo crear tickets de cambio en esta ejecución")
    if st.button("Ejecutar agente", type="primary"):
        with st.spinner("El agente está trabajando…"):
            r = ejecutar_agente(tarea, herramientas_guia(asis.indice), confirmar=lambda h, a: confirmar_tickets, max_pasos=6)
        (st.success if r.terminado else st.error)(r.respuesta)
        for p in r.pasos:
            with st.expander(f"Paso {p.n} · {p.propuesta.get('accion')} {p.propuesta.get('herramienta', '')} · {p.estado}"):
                st.json({"propuesta": p.propuesta, "resultado": p.resultado})
        if TICKETS:
            st.info(f"Tickets creados (simulados): {[t['folio'] for t in TICKETS]}")
