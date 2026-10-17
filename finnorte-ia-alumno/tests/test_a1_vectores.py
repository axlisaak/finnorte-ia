import numpy as np
import pytest
from conftest import pendiente

from finnorte.retrieval import Indice, coseno, normalizar


@pendiente("A1")
def test_normalizar_filas_unitarias():
    m = normalizar(np.array([[3.0, 4.0], [1.0, 0.0]]))
    assert np.allclose(np.linalg.norm(m, axis=1), 1.0)


@pendiente("A1")
def test_normalizar_vector_cero_no_explota():
    m = normalizar(np.array([[0.0, 0.0]]))
    assert np.all(np.isfinite(m)) and np.allclose(m, 0.0)


@pendiente("A1")
def test_coseno_casos_conocidos():
    assert coseno([1, 0], [1, 0]) == pytest.approx(1.0)
    assert coseno([1, 0], [0, 1]) == pytest.approx(0.0)
    assert coseno([1, 0], [-1, 0]) == pytest.approx(-1.0)
    assert coseno([1, 2], [2, 4]) == pytest.approx(1.0)  # misma dirección, distinta magnitud


@pendiente("A1")
def test_buscar_devuelve_k_ordenados():
    ind = Indice.desde_carpeta("corpus/comun")
    res = ind.buscar("rotación de secretos y llaves de API", k=3)
    assert 1 <= len(res) <= 3
    assert all(res[i].puntaje >= res[i + 1].puntaje for i in range(len(res) - 1))
    assert res[0].fragmento.doc_id == "ing-02"
