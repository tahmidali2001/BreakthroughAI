import game
import defense
import offense

##################### FOURTH MATCH UP ###############################
##  Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)  ##


def main():
    new_game = game.Game()
    current_player = new_game.PLAYER2
    agent_1 = offense.AlphaBeta(2)  # Player 1
    agent_2 = offense.AlphaBeta(1)  # Player 2
    winner = new_game.check_winner()
    new_game.print_board()

    while winner is None:
        #Set up game turn
        current_player = new_game.PLAYER1 if current_player == new_game.PLAYER2 else new_game.PLAYER2

        #Display
        if current_player == new_game.PLAYER1:
            print("Player 1 Turn!!!")
        else:
            print("Player 2 Turn!!!")

        #Decide who's turn it is
        if current_player == new_game.PLAYER1:
            best_move = agent_1.alphabeta_decision(new_game, current_player)
        else:
            best_move = agent_2.alphabeta_decision(new_game, current_player)

        #CHECK IF VALID
        valid = new_game.is_valid_move(best_move, current_player)
        while valid is False:
            print("INVALID, TRY AGAIN!!")
            if current_player == new_game.PLAYER1:
                best_move = agent_1.alphabeta_decision(new_game, current_player)
            else:
                best_move = agent_2.alphabeta_decision(new_game, current_player)

            valid = new_game.is_valid_move(best_move, current_player)
            print("Move: ", best_move)

        #Move piece, check status and print board
        new_game.move_piece(best_move, current_player)
        winner = new_game.check_winner()
        new_game.print_board()

    #After exiting the loop print who wins
    if winner is True:
        print("PLAYER 1 WINS!!!!!")
    else:
        print("PLAYER 2 WINS!!!!!")

if __name__ == "__main__":
  main()