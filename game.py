## GAME BOARD USING PYGAME ##
class Game:
    # Constants
    BOARD_SIZE = 8
    PLAYER1 = '*'
    PLAYER2 = '.'

    def __init__(self):
        self.board = [[self.PLAYER1 if row < 2 else self.PLAYER2 if row > 5 else ' '\
                       for _ in range(self.BOARD_SIZE)] for row in range(self.BOARD_SIZE)
    ]
        self.game_over = None


    def print_board(self):
        # Print column indices
        print('   ', end='')
        for col in range(self.BOARD_SIZE):
            print(f'{col} ', end='')
        print()
        # Print board rows with row indices
        for row, row_content in enumerate(self.board):
            print(f'{row}  ', end='')
            print(' '.join(row_content))
        print()

    def is_valid_move(self, move, player):
        current_row, current_col = move[0]
        new_row, new_col = move[1]
        # Check if the move is within the bounds of the board
        if not (0 <= new_row < self.BOARD_SIZE and 0 <= new_col < self.BOARD_SIZE):
            return False
          
        # Check is space is empty, if not then check if opponent piece
        if self.board[new_row][new_col] != ' ':
            if self.board[new_row][new_col] != player and abs(new_col - current_col) == 1:
                return True
            else:
                return False
              
        # Check if the move is forward for the player
        if player == self.PLAYER1:
            if new_row <= current_row:
                return False
        elif player == self.PLAYER2:
            if new_row >= current_row:
                return False
              
        # Check if the move is right or left diagonal
        if abs(new_row - current_row) != 1 or abs(new_col - current_col) > 1:
            return False

        return True

    # Function to make a move with row, col
    def make_move(self, row, col, new_row, new_col, player):
      self.board[row][col] = ' '
      self.board[new_row][new_col] = player

    # Function to make a move
    def move_piece(self, move, player):
      row, col = move[0]
      new_row, new_col = move[1]
      self.board[row][col] = ' '
      self.board[new_row][new_col] = player

    # Function to check if a player has won True = player1, False = player2
    def check_winner(self):
        player1_count = self.current_pieces
        player2_count = self.current_pieces

        if player1_count == 0:
            self.game_over = True
            return self.game_over
        elif player2_count == 0:
            self.game_over = False
            return self.game_over


        if self.PLAYER2 in self.board[0]:
            self.game_over = False
            return self.game_over
        elif self.PLAYER1 in self.board[self.BOARD_SIZE - 1]:
            self.game_over = True
            return self.game_over

        return None


    def current_pieces(self, player):
        if player == self.PLAYER1:
            pieces = sum(row.count(self.PLAYER1) for row in self.board)
        else:
            pieces = sum(row.count(self.PLAYER2) for row in self.board)
        return pieces

    def get_board_state(self):
        return [row[:] for row in self.board]

    def actions(self, board, player):
        actions = []

        # Iterate over all positions on the board
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):

                # Check if the current position belongs to the specified player
                if board[row][col] == player:
                    possible_moves = []

                    # Check left diagonal
                    if player == self.PLAYER1:
                        if 0 <= row + 1 < self.BOARD_SIZE and 0 <= col + 1 < self.BOARD_SIZE:
                            if board[row + 1][col + 1] == ' ' or board[row + 1][col + 1] != player:
                                possible_moves.append(((row + 1, col + 1)))
                    else:
                        if 0 <= row - 1 < self.BOARD_SIZE and 0 <= col + 1 < self.BOARD_SIZE:
                            if board[row - 1][col + 1] == ' ' or board[row - 1][col + 1] != player:
                                possible_moves.append(((row - 1, col + 1)))                        

                    # Check right diagonal
                    if player == self.PLAYER1:
                        if 0 <= row + 1 < self.BOARD_SIZE and 0 <= col - 1 < self.BOARD_SIZE:
                            if board[row + 1][col - 1] == ' ' or board[row + 1][col - 1] != player:
                                possible_moves.append(((row + 1, col - 1)))
                    else:
                         if 0 <= row - 1 < self.BOARD_SIZE and 0 <= col - 1 < self.BOARD_SIZE:
                            if board[row - 1][col - 1] == ' ' or board[row - 1][col - 1] != player:
                                possible_moves.append(((row - 1, col - 1)))

                    # Check forward
                    if player == self.PLAYER1:
                        if 0 <= row + 1 < self.BOARD_SIZE and board[row + 1][col] == ' ':
                            possible_moves.append(((row + 1, col)))
                    elif player == self.PLAYER2:
                        if 0 <= row - 1 < self.BOARD_SIZE and board[row - 1][col] == ' ':
                            possible_moves.append(((row - 1, col)))

                    if len(possible_moves) != 0:
                         actions.append([(row, col)] + possible_moves)
        return actions
