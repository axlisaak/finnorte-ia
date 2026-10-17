import json

from conftest import pendiente

from finnorte import controles, llm
from finnorte.asistente import Asistente
from finnorte.retrieval import Fragmento, Resultado


def _res(id_, p=0.8):
    return Resultado(Fragmento(id_, id_.split("#")[0], "t", "texto", {}), p)


@pendiente("Avance 1")
def test_citas_inventadas_se_detectan():
    rec = [_res("ing-02#0"), _res("ing-03#0")]
    assert controles.verificar_citas(["ing-02#0"], rec) == []
    assert controles.verificar_citas(["ing-02"], rec) == []          # basta el id del documento
    assert controles.verificar_citas(["ing-99#0"], rec)               # alucinada
    assert controles.verificar_citas([], rec)                         # no citó nada


@pendiente("Avance 1")
def test_abstencion_por_umbral():
    assert controles.debe_abstenerse([], 0.3)
    assert controles.debe_abstenerse([_res("a#0", 0.2)], 0.3)
    assert not controles.debe_abstenerse([_res("a#0", 0.5)], 0.3)


@pendiente("Avance 1")
def test_asistente_rechaza_cita_alucinada():
    llm.fake.responder = lambda p, s: json.dumps({"respuesta": "Se rotan cada semana", "fuentes": ["ing-99#0"], "abstuvo": False})
    a = Asistente.crear(umbral=0.0)
    out = a.responder("¿Cada cuánto se rotan los secretos?")
    assert out["abstuvo"] and out["errores_citas"]
