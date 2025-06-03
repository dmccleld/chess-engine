from ChessBoard import ChessBoard

def test_board_cloning(chess_board):
    # Clone the board
    cloned_board = chess_board.clone()

    # Make a move on the original board
    # Example move: Move a pawn from e2 to e4
    chess_board.move_piece((6, 4), (4, 4))

    # Compare the boards
    for rank in range(8):
        for file in range(8):
            original_piece = chess_board.board[rank][file].piece
            cloned_piece = cloned_board.board[rank][file].piece

            # Check if the pieces are the same
            if original_piece is not None or cloned_piece is not None:
                # Check if both squares have a piece and if they are the same type and color
                if original_piece is None or cloned_piece is None or \
                   original_piece.type != cloned_piece.type or \
                   original_piece.color != cloned_piece.color:
                    print(f"Difference found at position {(rank, file)}")
                    return False

    print("Cloning successful. No differences found.")
    return True

chess_board = ChessBoard()

test_board_cloning(chess_board)