from positional_data import *
import random

class Player:
    def __init__(self, color, human=True) -> None:
        self.color = color
        self.move = 0
        self.endgame = 0
        self.human = human
        self.pruning_counter = 0
        self.choose_opening()  # Initialize the opening book when creating a Player
        
    def valid_moves(self, chess_board, color):
        board = chess_board.board
        all_valid_moves = []
        for rank in range(8):
            for file in range(8):
                cell = board[rank][file]
                if cell.piece and color == cell.piece.color:
                    start = (rank, file)
                    for i in range(8):
                        for j in range(8):
                            end = (i, j)
                            if cell.piece.is_valid_move(start, end, chess_board):
                                all_valid_moves.append((start, end))
        return all_valid_moves
    
    def sort_valid_moves(self, valid_moves, chess_board):
        def orderer(move):
            future_board = chess_board.clone()
            future_board.push(move[0], move[1])
            return self.score_chessboard(future_board)

        sorted_valid_moves = sorted(valid_moves, key=orderer, reverse=(self.color=='white'))
        return sorted_valid_moves
    
    def score_chessboard(self, chess_board):
        # Check for checkmate/stalemate
        if chess_board.game_over:
            if chess_board.is_checkmate:
                return float('-inf') if chess_board.to_move == self.color else float('inf')
            return 0  # Draw

        white_score = 0
        black_score = 0
        
        # Detect endgame when material is low
        total_material = 0
        for row in chess_board.board:
            for cell in row:
                if cell.piece and cell.piece.type != 'king':
                    total_material += piece_values.get(cell.piece.type, 0)
        
        self.endgame = 1 if total_material < 30 else 0

        for row in chess_board.board:
            for cell in row:
                piece = cell.piece
                if piece:
                    value = piece_values.get(piece.type, 0)
                    if piece.color == 'white':
                        white_score += value
                        white_score += postional_values(piece.type, self.endgame, 'white')[piece.coord[0]][piece.coord[1]]
                    else:
                        black_score += value
                        black_score += postional_values(piece.type, self.endgame, 'black')[piece.coord[0]][piece.coord[1]]
        
        return white_score - black_score if self.color == 'white' else black_score - white_score

    def quiescence(self, chess_board, alpha, beta, depth=4):
        stand_pat = self.score_chessboard(chess_board)
        
        if depth == 0:
            return stand_pat
        
        if stand_pat >= beta:
            return beta
        
        alpha = max(alpha, stand_pat)
        
        # Only consider captures
        for move in self.sort_valid_moves(self.valid_moves(chess_board, chess_board.to_move), chess_board):
            if chess_board.is_capture(move[0], move[1]):
                future_board = chess_board.clone()
                future_board.push(move[0], move[1])
                score = -self.quiescence(future_board, -beta, -alpha, depth - 1)
                
                if score >= beta:
                    return beta
                alpha = max(alpha, score)
        
        return alpha

    def minimax(self, chess_board, depth, alpha, beta, is_maximizing_player):
        if depth == 0 or chess_board.game_over:
            return self.quiescence(chess_board, alpha, beta)
        
        valid_moves = self.valid_moves(chess_board, chess_board.to_move)
        if not valid_moves:  # No valid moves available
            return float('-inf') if is_maximizing_player else float('inf')

        if is_maximizing_player:
            max_eval = float('-inf')
            for move in self.sort_valid_moves(valid_moves, chess_board):
                future_board = chess_board.clone()
                future_board.push(move[0], move[1])
                eval = self.minimax(future_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    self.pruning_counter += 1
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.sort_valid_moves(valid_moves, chess_board):
                future_board = chess_board.clone()
                future_board.push(move[0], move[1])
                eval = self.minimax(future_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    self.pruning_counter += 1
                    break
            return min_eval

    def choose_opening(self):
        # Simple opening book
        self.opening_book = {
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -": [
                ((6, 4), (4, 4)),  # e4
                ((6, 3), (4, 3)),  # d4
            ],
            # Add more opening positions and moves as needed
        }

    def get_opening_move(self, chess_board):
        fen = chess_board.get_fen()
        if fen in self.opening_book:
            return random.choice(self.opening_book[fen])
        return None

    def select_move(self, chess_board, depth):
        # Try opening book first
        opening_move = self.get_opening_move(chess_board)
        if opening_move:
            return opening_move
            
        self.pruning_counter = 0
        valid_moves = self.valid_moves(chess_board, self.color)
        if not valid_moves:
            return None
            
        best_score = float('-inf')
        best_move = valid_moves[0]  # Default to first valid move
        
        for move in self.sort_valid_moves(valid_moves, chess_board):
            future_board = chess_board.clone()
            future_board.push(move[0], move[1])
            score = self.minimax(future_board, depth - 1, float('-inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move