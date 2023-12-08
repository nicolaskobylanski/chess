import pygame
import sys
from constantes import *
from juego import Game
from casilla import Square
from movimiento import Move

class Main:
    """
        Script principal del juego. El juego se ejecuta aquí.
    """
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):

        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board

        while True:
            game.show_background(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            # Manejo de todos los eventos
            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Arrastrar pieza
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_movs(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            game.show_background(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
            
                elif event.type == pygame.MOUSEMOTION:
                    # Mostrar la pieza mientras se arrastra
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Cambio virtual y real de la pieza arrastrada
                    if dragger.dragging: 
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQUARE_SIZE
                        released_col = dragger.mouseX // SQUARE_SIZE
                        
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            game.show_background(screen)
                            game.show_pieces(screen)

                            game.next_turn()

                    dragger.undrag_piece()

                if event.type == pygame.KEYDOWN:
                    # F para rendirse
                    if event.key == pygame.K_f:
                        print("You forfeited!")
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.mainloop()