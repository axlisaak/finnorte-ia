import time
import yaml


def leer_config(texto):
    return yaml.load(texto)


def token_valido(token, guardado, expira):
    return token == guardado and time.time() < expira
