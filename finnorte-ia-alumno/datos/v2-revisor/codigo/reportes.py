import logging
import pickle
import subprocess

log = logging.getLogger(__name__)


def cargar_reporte(datos_bytes):
    return pickle.loads(datos_bytes)


def exportar(nombre_archivo):
    subprocess.run(f"zip reportes.zip {nombre_archivo}", shell=True)


def registrar_cliente(cliente):
    log.info(f"cliente {cliente['nombre']} curp={cliente['curp']} clabe={cliente['clabe']}")
