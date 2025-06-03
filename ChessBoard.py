from typing import List, Tuple, Optional, Dict
from Cell import Cell
from Pieces import Piece

class ChessBoard:
    BOARD_SIZE = 8
    PIECE_SYMBOLS = {
        'white': {
            'pawn': '♙', 'rook': '♖', 'knight': '♘',
            'bishop': '♗', 'queen': '♕', 'king': '♔'
        },
        'black': {
            'pawn': '♟', 'rook': '♜', 'knight': '♞',
            'bishop': '♝', 'queen': '♛', 'king': '♚'
        }
    }

    def __init__(self) -> None:
        self.board: List[List[Cell]] = [[Cell() for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.initialize_pieces()
        self.to_move: str = 'white'
        self.game_over: bool = False
  
    def initialize_pieces(self):
        #pawns
        for i in range(8):
            self.board[1][i] = Cell(Piece('pawn', 'white', (1, i)))
            self.board[6][i] = Cell(Piece('pawn', 'black', (6, i)))
        #rooks
        for i in range(0,8,7):
            self.board[0][i] = Cell(Piece('rook', 'white', (0, i)))
            self.board[7][i] = Cell(Piece('rook', 'black', (7, i)))
        #knights
        for i in range(1,7,5):
            self.board[0][i] = Cell(Piece('knight', 'white', (0, i)))
            self.board[7][i] = Cell(Piece('knight', 'black', (7, i)))
        #bishops
        for i in range(2,6,3):
            self.board[0][i] = Cell(Piece('bishop', 'white', (0, i)))
            self.board[7][i] = Cell(Piece('bishop', 'black', (7, i)))
        #queen and kings
        self.board[0][3] = Cell(Piece('queen', 'white', (0, 3)))
        self.board[7][3] = Cell(Piece('queen', 'black', (7, 3)))
        self.board[0][4] = Cell(Piece('king', 'white', (0, 4)))
        self.board[7][4] = Cell(Piece('king', 'black', (7, 4)))

    def disp_board(self):
        pieces = {
            'white': { 
                'pawn': '♙', 'rook': '♖', 'knight': '♘',
                'bishop': '♗', 'queen': '♕', 'king': '♔'
            },
            'black': {
                'pawn': '♟', 'rook': '♜', 'knight': '♞',
                'bishop': '♝', 'queen': '♛', 'king': '♚'
            }
        }

        to_print_board = [['[ ]' for _ in range(8)] for _ in range(8)]

        for i in range(8):
            for j in range(8):
                if self.board[i][j].piece:
                    piece = self.board[i][j].piece
                    to_print_board[i][j] = '[' + pieces[piece.color][piece.type.lower()] + ']'

        to_print_board = to_print_board[::-1]

        row_label = 7
        column_label = '   0   1   2   3   4   5   6   7 '
        for row in to_print_board:
            print(row_label, ' '.join(row))
            row_label -= 1
        print(column_label)
    
    def handle_promote(self, end: Tuple[int, int]) -> str:
        """Handle pawn promotion with input validation."""
        valid_promotions = {
            'q': 'queen', 'r': 'rook', 
            'k': 'knight', 'b': 'bishop'
        }
        
        try:
            choice = input('Select promotion piece [Q)ueen R)ook K)night B)ishop]: ').lower()
            piece_type = valid_promotions.get(choice, 'queen')  # Default to queen if invalid input
            self.board[end[0]][end[1]].piece.type = piece_type
            return choice
        except Exception:
            self.board[end[0]][end[1]].piece.type = 'queen'
            return 'q'
    
    def push(self, start, end):
        self.board[end[0]][end[1]].piece = self.board[start[0]][start[1]].piece
        self.board[end[0]][end[1]].piece.moved = True
        self.board[end[0]][end[1]].piece.coord = end
        self.board[start[0]][start[1]].piece = None

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int], player_color: str) -> bool:
        """
        Move a piece if the move is valid.
        Returns True if move was successful, False otherwise.
        """
        start_cell = self.board[start[0]][start[1]]
        if not start_cell.piece or start_cell.piece.color != player_color:
            return False

        if start_cell.piece.is_valid_move(start, end, self):
            self._execute_move(start, end)
            
            # Handle pawn promotion
            end_piece = self.board[end[0]][end[1]].piece
            if end_piece.type == 'pawn' and (end[0] == 0 or end[0] == self.BOARD_SIZE - 1):
                print(f'{end_piece.type}:', start, end)
                self.handle_promote(end)
            
            return True
        return False

    def _execute_move(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """Execute the actual piece movement."""
        self.board[end[0]][end[1]].piece = self.board[start[0]][start[1]].piece
        self.board[end[0]][end[1]].piece.moved = True
        self.board[end[0]][end[1]].piece.coord = end
        self.board[start[0]][start[1]].piece = None

    def switch_players(self):
        self.to_move = 'black' if self.to_move == 'white' else 'white'
    
    def find_king(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece and piece.type == 'king' and piece.color == color:
                    return (i, j)
        return None
    
    def is_check(self, color: str) -> bool:
        """Determine if the specified color's king is in check."""
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        
        # Check all opponent pieces for attacks on king
        opponent_color = 'black' if color == 'white' else 'white'
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                piece = self.board[i][j].piece
                if piece and piece.color == opponent_color:
                    if piece.can_move_to((i, j), king_pos, self):
                        return True
        return False
    
    def is_mate(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece and piece.color == color:
                    for k in range(8):
                        for l in range(8):
                            if piece.is_valid_move((i, j), (k, l), self):
                                return False
        return True # mate

    def reset_pawn_flags(self):
        for row in self.board:
            for cell in row:
                if cell.piece and cell.piece.type == 'pawn' and cell.piece.color == self.to_move:
                    cell.piece.new_pawn_two_squares = False

    def clone(self):
        cloned_board = ChessBoard.__new__(ChessBoard)

        cloned_board.board = [[cell.clone() for cell in row] for row in self.board]
        cloned_board.to_move = self.to_move
        cloned_board.game_over = self.game_over

        return cloned_board

    def get_fen(self) -> str:
        """Returns the current board state in Forsyth–Edwards Notation (FEN)."""
        # Dictionary to map piece types to FEN characters
        fen_symbols = {
            ('white', 'pawn'): 'P', ('white', 'rook'): 'R',
            ('white', 'knight'): 'N', ('white', 'bishop'): 'B',
            ('white', 'queen'): 'Q', ('white', 'king'): 'K',
            ('black', 'pawn'): 'p', ('black', 'rook'): 'r',
            ('black', 'knight'): 'n', ('black', 'bishop'): 'b',
            ('black', 'queen'): 'q', ('black', 'king'): 'k'
        }
        
        fen_parts = []
        # Process board position
        for row in range(7, -1, -1):  # FEN starts from rank 8 (index 7)
            empty_squares = 0
            row_str = ''
            
            for col in range(8):
                piece = self.board[row][col].piece
                if piece is None:
                    empty_squares += 1
                else:
                    if empty_squares > 0:
                        row_str += str(empty_squares)
                        empty_squares = 0
                    row_str += fen_symbols[(piece.color, piece.type)]
            
            if empty_squares > 0:
                row_str += str(empty_squares)
            fen_parts.append(row_str)
        
        position = '/'.join(fen_parts)
        active_color = 'w' if self.to_move == 'white' else 'b'
        
        # For now, using placeholder values for castling and en passant
        # These could be implemented more accurately with additional tracking
        castling = 'KQkq'  # Assuming all castling rights available
        en_passant = '-'   # No en passant target
        halfmove = '0'     # Placeholder for halfmove clock
        fullmove = '1'     # Placeholder for fullmove number
        
        return f"{position} {active_color} {castling} {en_passant} {halfmove} {fullmove}"

    def is_capture(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Check if a move from start to end position results in a capture."""
        # Check if there's a piece at the end position
        end_piece = self.board[end[0]][end[1]].piece
        if not end_piece:
            # Special case: en passant capture for pawns
            if self.board[start[0]][start[1]].piece.type == 'pawn':
                if abs(end[1] - start[1]) == 1:  # Diagonal move
                    # Check for adjacent pawn that just moved two squares
                    adjacent_piece = self.board[start[0]][end[1]].piece
                    if (adjacent_piece and 
                        adjacent_piece.type == 'pawn' and 
                        adjacent_piece.color != self.board[start[0]][start[1]].piece.color and
                        adjacent_piece.new_pawn_two_squares):
                        return True
            return False
        
        # Regular capture: check if the end position has an opponent's piece
        return end_piece.color != self.board[start[0]][start[1]].piece.color