from agent import alpha_beta_bot, their_alpha_beta_bot
# TODO: feels like this shouldn't have to be imported
from board import IllegalMoveException
from game_state import GameState
from reversi_types import Move, Player
from utils import MalformedMoveCoordinatesException, print_move, print_board, point_from_coordinates
import time


def main():
    board_size = 8
    game = GameState.new_game(board_size)
    bot = alpha_beta_bot.AlphaBetaBot()
    # bot = their_alpha_beta_bot.AlphaBetaAgent(5, board.GameState.corner_evaluation_function)
    while not game.is_over():
        time.sleep(.1)
        print_board(game.board)
        if game.next_player == Player.black:
            move = None
            while not move:
                human_move = input("Enter your move:").strip()
                try:
                    move = Move.play(point_from_coordinates(human_move))
                except MalformedMoveCoordinatesException as e:
                    print(e)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        try:
            game = game.apply_move(move)
        except IllegalMoveException as e:
            print(e)
    results = game.get_result()
    for player, score in results.items():
        print("Player %s Score %d" % (player, score))


if __name__ == '__main__':
    main()

