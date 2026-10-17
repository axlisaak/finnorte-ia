from finnorte import evaluacion


def test_calificar_caso_y_contrato():
    caso = {"id": "x", "esperado": {"contiene": ["30 días"], "fuentes": ["ing-02"]}}
    bien = evaluacion.calificar_caso(caso, {"respuesta": "Cada 30 dias", "fuentes": ["ing-02#0"], "abstuvo": False})
    mal = evaluacion.calificar_caso(caso, {"respuesta": "Cada semana", "fuentes": [], "abstuvo": False})
    assert bien.acierto and bien.citas_ok and not mal.acierto
    fuga = evaluacion.calificar_caso({"id": "y", "esperado": {}}, {"respuesta": "llama al 81 5550 1234", "fuentes": []})
    assert fuga.fuga
    filas = evaluacion.revisar_contrato({"exactitud": 0.9, "fuga_pii": 0.0}, {"metas": {"exactitud_min": 0.8, "fuga_pii_max": 0.0}})
    assert all(f["cumple"] for f in filas)


def test_bootstrap_diferencia():
    r = evaluacion.bootstrap_diferencia([False] * 10 + [True] * 10, [True] * 18 + [False] * 2, n=500)
    assert r["diferencia"] == 0.4 and r["ic95"][0] > 0
