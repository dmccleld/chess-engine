from ChessBoard import ChessBoard
from AI import Player
from Utils import *

class GameController:
    def __init__(self) -> None:
        self.board = ChessBoard()
        self.players = {
            'white': Player('white'),
            'black': Player('black')
        }
    
    def handle_post_move(self):
        self.board.switch_players()

        if self.board.is_check(self.board.to_move):
            if self.board.is_mate(self.board.to_move):
                self.board.game_over = True
                print(f'Checkmate! {self.board.to_move.capitalize()} loses!')
            else:
                print('King is in check!')
        else:
            if self.board.is_mate(self.board.to_move):
                self.board.game_over = True
                print('Stalemate!')
    
    def get_valid_move_input(self):
        while True:
            try:
                move = input('Enter your piece\'s start position (row col): ')
                if not move.strip():  # Check for empty input
                    print("Invalid input! Please enter two numbers separated by space.")
                    continue
                start_position = tuple(map(int, move.split()))
                if is_valid_coordinate(start_position):
                    break
            except (ValueError, IndexError):
                print("Invalid input! Please enter two numbers separated by space.")
        
        while True:
            try:
                move = input('Enter your piece\'s end position (row col): ')
                if not move.strip():  # Check for empty input
                    print("Invalid input! Please enter two numbers separated by space.")
                    continue
                end_position = tuple(map(int, move.split()))
                if is_valid_coordinate(end_position):
                    break
            except (ValueError, IndexError):
                print("Invalid input! Please enter two numbers separated by space.")
        
        return start_position, end_position
    
    def start_game(self):
        white_ai = input('Should White be AI? (Y/N): ').lower()
        if white_ai == 'y':
            self.players['white'].human = False
        black_ai = input('Should Black be AI? (Y/N): ').lower()
        if black_ai == 'y':
            self.players['black'].human = False
        
        depth = 2
            
        while not self.board.game_over:
            # Display Board
            self.board.disp_board()
            
            self.board.reset_pawn_flags()
            print(f'{self.board.to_move.capitalize()} to Move!')

            if self.players[self.board.to_move].human:
                # Get input from the current player
                start_position, end_position = self.get_valid_move_input()
                
                if self.board.move_piece(start_position, end_position, self.board.to_move):
                    self.handle_post_move()
                else:
                    print('Invalid move, try again.')
            else:
                ai_move = self.players[self.board.to_move].select_move(self.board, depth)
                if ai_move:
                    start_position, end_position = ai_move
                    if self.board.move_piece(start_position, end_position, self.board.to_move):
                        print(f'AI moves from {start_position} to {end_position}')
                        self.handle_post_move()
                    else:
                        print('AI made invalid move, try again.')
                else:
                    print('AI could not find a valid move.')