import random
import game


## DUMMY HEURISTIC FOR OFFENSE ##
def calculate_heuristic1(current_game, player):
  player_pieces = current_game.current_pieces(player)
  cost = 2 * ((30 - player_pieces) + random.random())
  return cost


## OUR OFFENSIVE HEURISTIC ##
def calculate_heuristic2(current_game, player):
  advancement_score = 0

  # Evaluate each piece based on its proximity to the opponent's baseline
  for row in range(current_game.BOARD_SIZE):
    for col in range(current_game.BOARD_SIZE):
      if player == current_game.PLAYER2:
        if current_game.board[row][col] == player:
          # Since the opponent's baseline is at row 0, we use BOARD_SIZE - row to score advancement
          advancement_score += (current_game.BOARD_SIZE - row - 1)
        else:
          if current_game.board[row][col] == player:
            # Since the opponent's baseline is at row 0, we use BOARD_SIZE - row to score advancement
            advancement_score += (0 + row)

  # Optionally, include a small random factor to diversify moves slightly
  return advancement_score + random.uniform(0, 0.5)


## MINIMAX SEARCH AGENT ##
class MiniMax:

  def __init__(self, heuristic):
    self.maxdepth = 3
    self.heuristic = heuristic

  def max_value(self, current_game, player, depth):
    if depth == 0 or current_game.game_over is not None:
      if self.heuristic < 2:
        return calculate_heuristic1(current_game, player)
      else:
        return calculate_heuristic2(current_game, player)

    v = float('-inf')
    actions = current_game.actions(current_game.board, player)
    for action in actions:
      new_game = game.Game()  # Create a new instance for each action
      new_game.board = [row[:] for row in current_game.board]  # Copy the board
      initial_position = action[0]
      current_row, current_col = initial_position
      for move in action[1:]:
        new_row, new_col = move
        new_game.make_move(current_row, current_col, new_row, new_col, player)
      v = max(v, self.min_value(new_game, player, depth - 1))
    return v

  def min_value(self, current_game, player, depth):
    if depth == 0 or current_game.game_over is not None:
      if self.heuristic < 2:
        return calculate_heuristic1(current_game, player)
      else:
        return calculate_heuristic2(current_game, player)

    v = float('inf')
    actions = current_game.actions(current_game.board, player)
    for action in actions:
      new_game = game.Game()  # Create a new instance for each action
      new_game.board = [row[:] for row in current_game.board]  # Copy the board
      initial_position = action[0]
      current_row, current_col = initial_position
      for move in action[1:]:
        new_row, new_col = move
        new_game.make_move(current_row, current_col, new_row, new_col, player)
      v = min(v, self.max_value(new_game, player, depth - 1))
    return v

  def minimax_decision(self, current_game, player):
    best_action = None

    if player == current_game.PLAYER1:
      best_value = float('-inf')
      actions = current_game.actions(current_game.board, player)

      for action in actions:
        # Create a new instance for each action
        new_game = game.Game()
        # Copy the board
        new_game.board = [row[:] for row in current_game.board]
        initial_position = action[0]
        current_row, current_col = initial_position
        for move in action[1:]:
          new_row, new_col = move
          new_game.make_move(current_row, current_col, new_row, new_col,
                             player)
          value = self.min_value(new_game, player, self.maxdepth)
          if value > best_value:
            best_value = value
            best_action = [initial_position, move]
    else:
      best_value = float('inf')
      actions = current_game.actions(current_game.board, player)
      for action in actions:
        # Create a new game instance for each action
        new_game = game.Game()
        # Copy the board
        new_game.board = [row[:] for row in current_game.board]
        initial_position = action[0]
        for move in action[1:]:
          new_row, new_col = move
          current_row, current_col = initial_position
          new_game.make_move(current_row, current_col, new_row, new_col,
                             player)
          value = self.max_value(new_game, player, self.maxdepth)
          if value < best_value:
            best_value = value
            best_action = [initial_position, move]

    return best_action


## ALPHA-BETA SEARCH AGENT ##
class AlphaBeta:

  def __init__(self, heuristic):
    self.maxdepth = 3
    self.alpha = float('-inf')
    self.beta = float('inf')
    self.heuristic = heuristic

  def max_value(self, current_game, player, depth, alpha, beta):
    if depth == 0 or current_game.game_over is not None:
      if self.heuristic < 2:
        return calculate_heuristic1(current_game, player), None
      else:
        return calculate_heuristic2(current_game, player), None

    v = float('-inf')
    best_action = None
    actions = current_game.actions(current_game.board, player)
    for action in actions:
      new_game = game.Game()
      new_game.board = [row[:] for row in current_game.board]
      initial_position = action[0]
      current_row, current_col = initial_position
      for move in action[1:]:
        new_row, new_col = move
        new_game.make_move(current_row, current_col, new_row, new_col, player)
      value, _ = self.min_value(new_game, player, depth - 1, alpha, beta)
      if value > v:
        v = value
        best_action = action
      if v >= beta:
        return v, best_action
      alpha = max(alpha, v)
    return v, best_action

  def min_value(self, current_game, player, depth, alpha, beta):
    if depth == 0 or current_game.game_over is not None:
      if self.heuristic < 2:
        return calculate_heuristic1(current_game, player), None
      else:
        return calculate_heuristic2(current_game, player), None

    v = float('inf')
    best_action = None
    actions = current_game.actions(current_game.board, player)
    for action in actions:
      new_game = game.Game()
      new_game.board = [row[:] for row in current_game.board]
      initial_position = action[0]
      current_row, current_col = initial_position
      for move in action[1:]:
        new_row, new_col = move
        new_game.make_move(current_row, current_col, new_row, new_col, player)
      value, _ = self.max_value(new_game, player, depth - 1, alpha, beta)
      if value < v:
        v = value
        best_action = action
      if v <= alpha:
        return v, best_action
      beta = min(beta, v)
    return v, best_action

  def alphabeta_decision(self, current_game, player):
    best_action = self.max_value(current_game, player, self.maxdepth,
                                 self.alpha, self.beta)[1]
    if best_action is not None:
      start_position = best_action[0]
      new_position = best_action[-1]
      return start_position, new_position
    else:
      return None, None
