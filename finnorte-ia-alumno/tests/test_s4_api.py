import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402
from conftest import pendiente  # noqa: E402


@pytest.fixture
def cliente(monkeypatch):
    monkeypatch.setenv("API_KEY", "secreta-de-prueba")
    import api.main as m
    m._asistente = None
    m._ventanas.clear()
    return TestClient(m.app)


def test_salud(cliente):
    assert cliente.get("/salud").json()["estado"] == "ok"


def test_sin_llave_401_problem_json(cliente):
    r = cliente.post("/v1/preguntas", json={"pregunta": "¿Cada cuánto se rotan los secretos?"})
    assert r.status_code == 401 and r.headers["content-type"].startswith("application/problem+json")
    assert {"type", "title", "status", "detail", "trace_id"} <= set(r.json())


@pendiente("Avance 1")
def test_pregunta_valida(cliente):
    r = cliente.post("/v1/preguntas", json={"pregunta": "¿Cada cuánto se rotan los secretos?"},
                     headers={"X-API-Key": "secreta-de-prueba"})
    assert r.status_code == 200 and "fuentes" in r.json()


def test_validacion_de_entrada(cliente):
    r = cliente.post("/v1/preguntas", json={"pregunta": "x"}, headers={"X-API-Key": "secreta-de-prueba"})
    assert r.status_code == 422
