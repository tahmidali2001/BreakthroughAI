import random
import sys

  # GAME BOARD USING PYGAME
class Game:
      # Constants
    BOARD_SIZE = 8
    PLAYER1 = '*'
    PLAYER2 = '.'

    def __init__(self):
        self.board = [[self.PLAYER1 if row < 2 else self.PLAYER2 if row > 5 else ' ' \
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

    def is_valid_move(self, current_row, current_col, new_row, new_col, player):
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

    # Function to make a move
    def make_move(self, current_row, current_col, new_row, new_col, player):
        self.board[current_row][current_col] = ' '
        self.board[new_row][new_col] = player

    # Function to check if a player has won True = player1, False = player2
    def check_winner(self):
        player1_count = self.current_pieces
        player2_count = self.current_pieces

        if player1_count == 0:
            self.game_over = False
            return self.game_over
        elif player2_count == 0:
            self.game_over = True
            return self.game_over


        if self.PLAYER2 in self.board[0]:
            self.game_over = False
            return self.game_over
        elif self.PLAYER1 in self.board[self.BOARD_SIZE - 1]:
            self.game_over = True
            return self.game_over

        return None

    def receive_move(self, player):
      # THIS IS FOR THE GAME CLASS TO RECIEVE A MOVE FROM THE AI AGENT
        self.print_board() # REMOVE
        if player == self.PLAYER1: # REMOVE
            print(f"Player 1, make your move!") # REMOVE
            print("Enter current row, current col, new row, new col (separated by spaces):")
        else:
            print(f"Player 2, make your move!") # REMOVE
            print("Enter current row, current col, new row, new col (separated by spaces):") #REMOVE
        move = input().split() # REMOVE

        return [int(coord) for coord in move]

    def current_pieces(self, player):
        if player == game.PLAYER1:
            pieces = sum(row.count(self.PLAYER1) for row in self.board)
        else:
            pieces = sum(row.count(self.PLAYER2) for row in self.board)
        return pieces

    def get_board_state(self):
        return [row[:] for row in self.board]

    def actions(self, position, player):
        row, col = position
        actions = []

        # Check right diagonal
        if player == self.PLAYER1 or player == self.PLAYER2:
            if 0 <= row - 1 < self.BOARD_SIZE and 0 <= col + 1 < self.BOARD_SIZE and self.board[row - 1][col + 1] == ' ':
                actions.append((row - 1, col + 1))
            if 0 <= row + 1 < self.BOARD_SIZE and 0 <= col + 1 < self.BOARD_SIZE and self.board[row + 1][col + 1] == ' ':
                actions.append((row + 1, col + 1))

        # Check left diagonal
        if player == self.PLAYER1 or player == self.PLAYER2:
            if 0 <= row - 1 < self.BOARD_SIZE and 0 <= col - 1 < self.BOARD_SIZE and self.board[row - 1][col - 1] == ' ':
                actions.append((row - 1, col - 1))
            if 0 <= row + 1 < self.BOARD_SIZE and 0 <= col - 1 < self.BOARD_SIZE and self.board[row + 1][col - 1] == ' ':
                actions.append((row + 1, col - 1))

        # Check forward
        if player == self.PLAYER1:
            if 0 <= row +2 < self.BOARD_SIZE and self.board[row + 1][col] == ' ':
                actions.append((row + 1, col))
        elif player == self.PLAYER2:
            if 0 <= row - 1 < self.BOARD_SIZE and self.board[row - 1][col] == ' ':
                actions.append((row - 1, col))

        return actions


#TEST
if __name__ == "__main__":
  game = Game()
  current_player = game.PLAYER1
  game.print_board()
  position = [1, 1]
  actions = game.actions(position, current_player)
  print("Possible actions: ", actions)