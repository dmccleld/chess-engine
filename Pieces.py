class Piece:
    def __init__(self, type, color, coord) -> None:
        self.type = type
        self.color = color
        self.moved = False
        self.new_pawn_two_squares = False
        self.coord = coord
    
    def is_valid_move(self, start, end, chess_board):
        # Clone to prevent board change
        future_board = chess_board.clone()

        if not self.can_move_to(start, end, future_board):
            return False

        # Store original positions
        original_piece = future_board.board[end[0]][end[1]].piece
        future_board.board[end[0]][end[1]].piece = self.clone()
        future_board.board[start[0]][start[1]].piece = None

        # Check for check
        in_check = future_board.is_check(self.color)

        # Undo the move
        future_board.board[start[0]][start[1]].piece = self.clone()
        future_board.board[end[0]][end[1]].piece = original_piece

        if in_check:
            return False
        
        return True

    def can_move_to(self, start, end, chess_board):    
        if self.type == 'pawn':
            return self.is_valid_pawn_move(start, end, chess_board.board)
        if self.type == 'rook':
            return self.is_valid_rook_move(start, end, chess_board.board)
        if self.type == 'knight':
            return self.is_valid_knight_move(start, end, chess_board.board)
        if self.type == 'bishop':
            return self.is_valid_bishop_move(start, end, chess_board.board)
        if self.type == 'queen':
            return self.is_valid_queen_move(start, end, chess_board.board)
        if self.type == 'king':
            return self.is_valid_king_move(start, end, chess_board)
    
    def is_valid_pawn_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        direction = 1 if self.color == 'white' else -1 # Determines forward direction

        # En passant capture condition
        if abs(dy) == 1 and dx == direction: # diagnol move
            # Target square is empty (en passant condition)
            if not board[end[0]][end[1]].piece:
                adjacent_pawn_row = start[0]
                adjacent_pawn_col = end[1]
                adjacent_pawn = board[adjacent_pawn_row][adjacent_pawn_col].piece
                if adjacent_pawn and adjacent_pawn.type == 'pawn' and adjacent_pawn.new_pawn_two_squares and adjacent_pawn.color != self.color:
                    board[adjacent_pawn_row][adjacent_pawn_col].piece = None # capture the pawn
                    return True
        
        if dy == 0: #forward move
            if dx == direction and not board[end[0]][end[1]].piece:
                return True
            if (start[0]==1 or start[0]==6) and (dx == 2*direction) and not board[end[0]][end[1]].piece and not board[start[0]+direction][start[1]].piece:
                self.new_pawn_two_squares = True
                return True
        
        # diagnol move
        if abs(dy) == 1 and dx == direction:
            # check if there is a piece of opposite color
            if board[end[0]][end[1]].piece:
                return self.color != board[end[0]][end[1]].piece.color
        
        return False

    def is_valid_rook_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
  
        # Check that the move is strictly horizontal or vertical
        if dx != 0 and dy != 0:
            return False
        
        # Determine step direction for iteration
        xdirection = 1 if dx > 0 else -1 if dx < 0 else 0
        ydirection = 1 if dy > 0 else -1 if dy < 0 else 0

        # Horizontal Move
        if dx == 0:
            # Check if piece in between
            for i in range(1, abs(dy)):
                travel = i * ydirection
                if board[end[0]][start[1]+travel].piece:
                    return False
            # Check capture condition at the destination
            if board[end[0]][end[1]].piece and self.color == board[end[0]][end[1]].piece.color:
                return False
            return True

        # Vertical Move
        if dy == 0:
            for i in range(1, abs(dx)):
                travel = i * xdirection
                if board[start[0]+travel][end[1]].piece:
                    return False
            # Check capture condition at the destination
            if board[end[0]][end[1]].piece and self.color == board[end[0]][end[1]].piece.color:
                return False
            return True
                

    def is_valid_knight_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check L pattern
        if not ((abs(dx) == 2 and abs(dy) == 1) or (abs(dx) == 1 and abs(dy) == 2)):
            return False
        
        # Check capture condition at the destination
        if board[end[0]][end[1]].piece and self.color == board[end[0]][end[1]].piece.color:
            return False
        return True


    def is_valid_bishop_move(self, start, end, board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Check that it is only diagnol
        if not (abs(dx) == abs(dy) and abs(dx) > 0):
            return False
        
        xdirection = 1 if dx > 0 else -1
        ydirection = 1 if dy > 0 else -1

        for i in range(1, abs(dy)):
            ytravel = i * ydirection
            xtravel = i * xdirection
            if board[start[0]+xtravel][start[1]+ytravel].piece:
                return False
        
        # Check capture condition at the destination
        if board[end[0]][end[1]].piece and self.color == board[end[0]][end[1]].piece.color:
            return False
        return True
        

    def is_valid_queen_move(self, start, end, board):
        return self.is_valid_bishop_move(start, end, board) or self.is_valid_rook_move(start, end, board)
        
    def is_path_in_check(self, start, end, board):
        if board.is_check(self.color):
            return True
        
        dy = end[1] - start[1]

        direction = 1 if dy > 0 else -1

        for i in range(1, abs(dy)+1):
            y_position = start[1] + (i * direction)
            if self.is_square_attacked(start[0], y_position, board):
                return True
        return False

    def is_square_attacked(self, x, y, chess_board):
        # Check if the square at (x, y) is attacked by any of the opponent's pieces
        opponent_color = 'black' if self.color == 'white' else 'white'
        for i in range(8):
            for j in range(8):
                piece = chess_board.board[i][j].piece
                if piece and piece.color == opponent_color:
                    if piece.can_move_to((i, j), (x, y), chess_board):
                        return True
        return False
    
    def is_valid_king_move(self, start, end, chess_board):
        dx = end[0] - start[0]
        dy = end[1] - start[1]

        # Right side castle
        if (dx == 0 and dy == 2) and not self.moved and (chess_board.board[end[0]][5].piece == None) and (chess_board.board[end[0]][6].piece == None) and (chess_board.board[end[0]][7].piece) and chess_board.board[end[0]][7].piece.moved == False and not self.is_path_in_check(start, end, chess_board):
            chess_board.board[end[0]][5].piece = chess_board.board[end[0]][7].piece
            chess_board.board[end[0]][5].piece.moved = True
            chess_board.board[end[0]][7].piece = None
            return True
        # Left side castle
        if (dx == 0 and dy == -2) and not self.moved and (chess_board.board[end[0]][3].piece == None) and (chess_board.board[end[0]][2].piece == None) and (chess_board.board[end[0]][1].piece == None) and (chess_board.board[end[0]][0].piece) and chess_board.board[end[0]][0].piece.moved == False and not self.is_path_in_check(start, end, chess_board):
            chess_board.board[end[0]][3].piece = chess_board.board[end[0]][0].piece
            chess_board.board[end[0]][3].piece.moved = True
            chess_board.board[end[0]][0].piece = None
            return True
        
        # Can only move one space in all directions
        if not (max(abs(dx), abs(dy)) == 1):
            return False
        
        # Check capture condition
        if chess_board.board[end[0]][end[1]].piece and (self.color == chess_board.board[end[0]][end[1]].piece.color):
            return False

        return True
   
    def clone(self):
        
        cloned_piece = Piece(self.type, self.color, self.coord)

        cloned_piece.moved = self.moved

        cloned_piece.new_pawn_two_squares = self.new_pawn_two_squares

        return cloned_piece