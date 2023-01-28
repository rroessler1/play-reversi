from agent import random_bot, alpha_beta_bot, their_alpha_beta_bot
import board
import reversi_types
from utils import print_move, print_board, move_from_coordinates
import time


def main():
    board_size = 8
    game = board.GameState.new_game(board_size)
    bot = alpha_beta_bot.AlphaBetaBot()
    # bot = their_alpha_beta_bot.AlphaBetaAgent(5, board.GameState.corner_evaluation_function)
    while not game.is_over():
        time.sleep(.1)
        print_board(game.board)
        if game.next_player == reversi_types.Player.black:
            human_move = input("Enter your move:")
            move = board.Move.play(move_from_coordinates(human_move.strip()))
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        try:
            game = game.apply_move(move)
        except board.IllegalMoveException as e:
            print(e)
    results = game.get_result()
    for player, score in results.items():
        print("Player %s Score %d" % (player, score))


if __name__ == '__main__':
    main()

