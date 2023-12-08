import pygame
from constantes import *

class Dragger:
    """
        Script que se encarga de mostrar las piezas mientras son arrastradas 
        por el tablero.
    """

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0

    # Recoge la nueva posición de la pieza mientras que es arrastrada por el ratón
    def update_blit(self, surface):
        texture = self.piece.texture
        img = pygame.image.load(texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)

    # Actualiza posición del ratón
    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    # Guarda la casilla inicial de la pieza
    def save_initial(self, pos):
        self.initial_row = pos[1] // SQUARE_SIZE
        self.initial_col = pos[0] // SQUARE_SIZE

    # Pieza siendo arrastrada --> True
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    # Pieza siendo arrastrada --> False
    def undrag_piece(self):
        self.piece = None
        self.dragging = False