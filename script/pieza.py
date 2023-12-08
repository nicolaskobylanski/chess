import os

class Piece:
    """
        Este script incluye toda la información que guarda cada pieza. 
        El color, el png, una lista que guarda movimientos, étc...
    """

    def __init__(self, name, color, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    # png de cada pieza
    def set_texture(self):
        self.texture = os.path.join(
            f'CHESS/assets/{self.color}_{self.name}.png')
        
    # Añade movimiento a lista de movimientos
    def add_move(self, move):
        self.moves.append(move)

    # Reestablece la lista de movimientos
    def clear_moves(self):
        self.moves = []


# Clase de cada pieza que establece color y dirección en base al color
class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color)

class King(Piece):

    def __init__(self, color):
        super().__init__('king', color)