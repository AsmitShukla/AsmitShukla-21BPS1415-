class GameState:
    def __init__(self):
        self.board = [["" for _ in range(5)] for _ in range(5)]
        self.players = {'A': [], 'B': []}
        self.current_turn = 'A'
        self.initialize_game()

    def initialize_game(self):
        # Initialize player A pieces
        self.players['A'] = ['A-P1', 'A-P2', 'A-H1', 'A-H2', 'A-P3']
        for i, piece in enumerate(self.players['A']):
            self.board[0][i] = piece

        # Initialize player B pieces
        self.players['B'] = ['B-P1', 'B-P2', 'B-H1', 'B-H2', 'B-P3']
        for i, piece in enumerate(self.players['B']):
            self.board[4][i] = piece

    def move_piece(self, player, piece, move):
        # Implement the logic to move the piece, validate moves, and handle combat
        pass

    def is_valid_move(self, piece, move):
        # Implement move validation logic
        pass

    def get_game_state(self):
        return {
            'board': self.board,
            'current_turn': self.current_turn,
            'players': self.players
        }
