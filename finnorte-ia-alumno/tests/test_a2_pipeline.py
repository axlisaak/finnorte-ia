import json

from conftest import pendiente

from finnorte import llm
from finnorte.pipeline import Etapa, Pipeline, validar_esquema

SOLICITUD = "Agregar validación de Idempotency-Key al endpoint POST /v1/transferencias del servicio pagos-api."

RESPUESTAS = {
    "cambio_analizar": {"titulo": "Idempotencia en transferencias", "componentes": ["pagos-api"], "tipo": "funcionalidad",
                        "riesgo": "alto", "justificacion_riesgo": "Toca movimiento de dinero", "preguntas_abiertas": []},
    "cambio_plan": {"estrategia": "canary", "pasos": ["5 %", "50 %", "100 %"], "reversa": "Desactivar la bandera y revertir",
                    "aprobaciones": ["líder técnico", "operaciones"], "ventana": "martes 22:00"},
    "cambio_checklist": {"checklist": [{"punto": "Prueba con llave repetida", "origen": "analisis.componentes", "responsable": "qa"},
                                       {"punto": "Reversa probada", "origen": "plan.reversa", "responsable": "ops"},
                                       {"punto": "Canary observado 30 min", "origen": "plan.pasos", "responsable": "ops"}]},
    "cambio_nota": {"titulo": "Transferencias más seguras", "que_cambia": "Se evitan cobros duplicados",
                    "impacto_usuario": "Ninguno visible", "fecha_estimada": "NO ESPECIFICADO", "contacto": "equipo de ingeniería"},
}


def _falso(prompt, sistema):
    for clave, val in RESPUESTAS.items():
        if clave == "cambio_analizar" and "Solicitud de cambio" in prompt:
            return json.dumps(val)
        if clave == "cambio_plan" and "Reglas del plan" in prompt:
            return json.dumps(val)
        if clave == "cambio_checklist" and "verificarse con un sí/no" in sistema:
            return json.dumps(val)
        if clave == "cambio_nota" and "notas de liberación" in sistema:
            return json.dumps(val)
    return "{}"


FLUJO = Pipeline([
    Etapa("analizar", "cambio_analizar"),
    Etapa("plan", "cambio_plan", usa=["analizar"]),
    Etapa("checklist", "cambio_checklist", usa=["analizar", "plan"]),
    Etapa("nota", "cambio_nota", usa=["analizar", "plan"]),
], nombre="cambio")


def test_validar_esquema_detecta_errores():
    esquema = {"type": "object", "required": ["riesgo"], "properties": {"riesgo": {"enum": ["alto", "bajo"]}}}
    assert validar_esquema({"riesgo": "alto"}, esquema) == []
    assert validar_esquema({"riesgo": "enorme"}, esquema)
    assert validar_esquema(None, esquema)


@pendiente("A2")
def test_flujo_encadena_cuatro_etapas():
    llm.fake.responder = _falso
    res = FLUJO.ejecutar({"solicitud": SOLICITUD})
    assert res.ok, [e.errores for e in res.etapas]
    assert [e.nombre for e in res.etapas] == ["analizar", "plan", "checklist", "nota"]
    assert res.salidas["analizar"]["riesgo"] == "alto"


@pendiente("A2")
def test_reintenta_cuando_el_json_no_cumple():
    llamadas = []

    def malo_luego_bueno(prompt, sistema):
        llamadas.append(prompt)
        return "no soy json" if len(llamadas) == 1 else json.dumps(RESPUESTAS["cambio_analizar"])
    llm.fake.responder = malo_luego_bueno
    res = Pipeline([Etapa("analizar", "cambio_analizar", reintentos=1)]).ejecutar({"solicitud": SOLICITUD})
    assert res.ok and res.etapas[0].intentos == 2
    assert "no cumplió el formato" in llamadas[1]
