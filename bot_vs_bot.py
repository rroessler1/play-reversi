from agent import random_bot, mct_agent
from game_state import GameState
from reversi_types import Player
from utils import print_move, print_board
import time
import cProfile


def main():
    board_size = 8
    game = GameState.new_game(board_size)
    bots = {
        Player.black: mct_agent.MctAgent(),
        Player.white: mct_agent.MctAgent(),
    }
    move_count = 0
    while move_count < 2:
        time.sleep(.1)
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game.apply_move(bot_move)
        move_count += 1
    results = game.get_result()
    for player, score in results.items():
        print("Player %s Score %d" % (player, score))


if __name__ == '__main__':
    cProfile.run('main()')

