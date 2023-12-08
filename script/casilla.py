
class Square:
    """
        Este script comprueba todas las condiciones de las casillas (que son movimientos disponibles)
        para saber si un movimiento es legal o no.
    """
    
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    # Metodo igual (equal)
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # La casilla tiene una pieza?
    def has_piece(self):
        return self.piece != None
    
    # La casilla está vacía?
    def is_empty(self):
        return not self.has_piece()

    # La casilla tiene una pieza de tu mismo color?
    def has_team(self, color):
        return self.has_piece() and self.piece.color == color

    # La casilla tiene una pieza rival?
    def has_rival(self, color):
        return self.has_piece() and self.piece.color != color

    # La casilla está vacía o tiene una pieza rival?
    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_rival(color)

    """
        Comprueba si la casilla se encuentra dentro del 8x8
        (para no poder mover la pieza fuera del tablero). 
    """
    @staticmethod # El método estático se utiliza para poder acceder el método sin definir la clase
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
            
        return True