from decimal import Decimal, ROUND_HALF_EVEN

LIMITE_NIVEL_1 = Decimal("8000")
LIMITE_NIVEL_2 = Decimal("50000")


def validar_monto(monto: Decimal, nivel: int) -> bool:
    """Devuelve True si el monto es válido para el nivel de cuenta."""
    if monto <= 0 or monto != monto.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN):
        return False
    limite = LIMITE_NIVEL_2 if nivel == 2 else LIMITE_NIVEL_1
    return monto <= limite
