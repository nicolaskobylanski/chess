
class Move:
    """
        Devuelve el movimiento realizado por el jugador.
    """

    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    # Se utiliza el método eq (equal), pues el ordenador no sabe comparar si dos movimientos son iguales
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final