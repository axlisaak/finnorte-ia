import hashlib
import random


def crear_usuario(db, correo, password):
    h = hashlib.md5(password.encode()).hexdigest()
    db.insert("usuarios", {"correo": correo, "hash": h})
    codigo = random.randint(100000, 999999)
    return codigo


def verificar(db, correo, password):
    u = db.find("usuarios", correo=correo)
    return u and u["hash"] == hashlib.md5(password.encode()).hexdigest()
