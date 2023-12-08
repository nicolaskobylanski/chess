from constantes import *
from casilla import Square
from pieza import *
from movimiento import Move

class Board:
    """
        Este script contiene la mayoría de la lógica del juego. Mientras que los otros scripts 
        se encargar de mostrar la parte virtual (los pngs, los colores) aquí se realiza todo de manera real.
        Este script contiene el tablero y piezas virtuales y todos los movimientos legales de cada pieza.
    """

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    # Crear nuevo movimiento
    def move(self, piece, move):
        
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True
        piece.clear_moves()

        self.last_move = move

    # Compara el movimiento realizado con los movimientos legales (accede al método eq en move)
    def valid_move(self, piece, move):
        return move in piece.moves

    # Todos los movimientos legales
    def calc_movs(self, piece, row, col):
        def other_moves(increments):
                """
                    Se utiliza un único método para los movimientos de la torre, el alfil y la reina,
                    pues todos ellos se pueden mover todas las casillas que deseen pero con patrones diferentes.
                    Alfil --> +1 row, +1 col... Torre --> +1 row / +1 col... Reina es combinación de alfil y torre.
                """
                for increment in increments:
                    row_increment, col_increment = increment
                    possible_move_row = row + row_increment
                    possible_move_col = col + col_increment

                    while True:
                        if Square.in_range(possible_move_row, possible_move_col):
                            initial = Square(row, col)
                            final_piece = self.squares[possible_move_row][possible_move_col].piece
                            final = Square(possible_move_row, possible_move_col, final_piece)
                            move = Move(initial, final)

                            if self.squares[possible_move_row][possible_move_col].is_empty():
                                piece.add_move(move)

                            elif self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                                piece.add_move(move)
                                break
                                
                            elif self.squares[possible_move_row][possible_move_col].has_team(piece.color):
                                break
                        
                        else: break

                        possible_move_row = possible_move_row + row_increment
                        possible_move_col = possible_move_col + col_increment
        def pawn_moves():
                        """
                            Los movimientos del peón son un poco mas complejos, pues al ser de un color u otro
                            su dirección de movimiento cambia. Además debe detectar si tiene una pieza en frente o en su 
                            diagonal derecha u izquierda para poder capturar.
                        """
                        steps = 1 if piece.moved else 2

                        # Movimientos verticales
                        start = row + piece.dir
                        end = row + (piece.dir * (1 + steps))
                        for possible_move_row in range(start, end, piece.dir):
                            if Square.in_range(possible_move_row):
                                if self.squares[possible_move_row][col].is_empty():
                                
                                    initial = Square(row, col)
                                    final = Square(possible_move_row, col)
                                    
                                    move = Move(initial, final)
                                    piece.add_move(move)
                                else:
                                    break
                            else:
                                break

                        # Movimientos diagonales
                        possible_move_row = row + piece.dir
                        possible_move_cols = [col-1, col+1]
                        for possible_move_col in possible_move_cols:
                            if Square.in_range(possible_move_row, possible_move_col):
                                if self.squares[possible_move_row][possible_move_col].has_rival(piece.color):
                                    
                                    initial = Square(row, col)
                                    final = Square(possible_move_row, possible_move_col)
                                    move = Move(initial, final)
                                    piece.add_move(move)  

        def knight_moves():
                        """
                            Los movimientos del caballo son de los más simples, pues solo hay que detectar
                            si hay una pieza en su casilla final, ya que saltan piezas.
                        """
                        possible_moves = [(row-2, col+1), 
                                        (row-1, col+2), 
                                        (row+1, col+2), 
                                        (row+2, col+1), 
                                        (row-2, col-1), 
                                        (row-1, col-2), 
                                        (row+1, col-2), 
                                        (row+2, col-1)]
                        
                        for possible_move in possible_moves:
                            possible_move_row, possible_move_col = possible_move
                            if Square.in_range(possible_move_row, possible_move_col):
                                if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                                    initial = Square(row, col)
                                    final = Square(possible_move_row, possible_move_col)
                                    move = Move(initial, final)
                                    piece.add_move(move)
        def king_moves():
                        """
                            Los movimientos del rey son también muy simples (1 en cada dirección)
                            ya que esta versión del ajedrez no detecta ni jaques, ni puede enrocar.
                        """
                        possible_moves = [(row+1, col+1), 
                                        (row-1, col+1), 
                                        (row-1, col-1), 
                                        (row+1, col-1), 
                                        (row, col-1), 
                                        (row, col+1), 
                                        (row+1, col), 
                                        (row-1, col)]
                        
                        for possible_move in possible_moves:
                            possible_move_row, possible_move_col = possible_move
                            if Square.in_range(possible_move_row, possible_move_col):
                                if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                                    initial = Square(row, col)
                                    final = Square(possible_move_row, possible_move_col)
                                    move = Move(initial, final)
                                    piece.add_move(move)

        # Según que pieza esté seleccionada, se llama un método
        if isinstance(piece, Pawn):      
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            other_moves([
                (-1, 1), (-1, -1), (1, 1), (1, -1)
            ])

        elif isinstance(piece, Rook):
            other_moves([
                (-1, 0), (1, 0), (0, -1), (0, 1)
            ])

        elif isinstance(piece, Queen):
            # Torre + alfil
            other_moves([
                (-1, 1), (-1, -1), (1, 1), (1, -1),
                (-1, 0), (1, 0), (0, -1), (0, 1)
            ])

        elif isinstance(piece, King):
            king_moves()

    # Método que crea el tablero real
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    # Método que añade las piezas reales
    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0) 

        # Peones
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Caballos
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Alfiles
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color)) 
        
        # Torres
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Reinas
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # Reyes
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        