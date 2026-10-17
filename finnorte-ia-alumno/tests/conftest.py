"""Configuración común de pruebas: todo corre SIN red con el proveedor `fake` y embeddings `hash`.

Las pruebas de piezas que aún no implementas se marcan como SKIP («Pendiente: A2»)
en lugar de fallar: así tu CI está en verde desde el día 1 y cada entrega «enciende» sus pruebas.
"""
import functools
import os
import sys
from pathlib import Path

import pytest

os.environ["LLM_PROVIDER"] = "fake"
os.environ["EMB_PROVIDER"] = "hash"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


@pytest.fixture(autouse=True)
def _bitacora_temporal(tmp_path, monkeypatch):
    from finnorte import config as cfg
    original = cfg.Config.__post_init__

    def post(self):
        original(self)
        self.dir_trazas = tmp_path
    monkeypatch.setattr(cfg.Config, "__post_init__", post)
    from finnorte import llm
    llm.fake.responder = None
    yield


def pendiente(entrega):
    """Decorador: si la función bajo prueba lanza NotImplementedError, la prueba se omite."""
    def deco(fn):
        @functools.wraps(fn)
        def envoltura(*a, **k):
            try:
                return fn(*a, **k)
            except NotImplementedError:
                pytest.skip(f"Pendiente: {entrega}")
        return envoltura
    return deco
