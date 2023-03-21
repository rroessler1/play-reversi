import agent.random_bot
from game_state import GameState
from reversi_types import Player
from utils import print_move, print_board
import time


def main():
    board_size = 8
    game = GameState.new_game(board_size)
    bots = {
        Player.black: agent.random_bot.RandomBot(),
        Player.white: agent.random_bot.RandomBot(),
    }
    while not game.is_over():
        time.sleep(.1)
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)
    results = game.get_result()
    for player, score in results.items():
        print("Player %s Score %d" % (player, score))


if __name__ == '__main__':
    main()

