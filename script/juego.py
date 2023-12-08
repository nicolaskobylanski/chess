import pygame
from constantes import *
from tablero import Board
from arrastrar import Dragger

class Game:
    """
        Script que incluye los métodos gráficos;
        mostrar el tablero, las piezas, y los movimientos legales
    """
    
    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()

    # Mostrar tablero
    def show_background(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = LIGHT_BLUE
                else:
                    color = DARK_BLUE

                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    # Mostrar piezas
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)

    # Mostrar movimientos legales
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C84646'
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    # Único método no gráfico --> establece el turno de cada jugador, por defecto blanco
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'