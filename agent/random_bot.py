import random
from agent.base import Agent
from board import Move
from reversi_types import Point


class RandomBot(Agent):
    def select_move(self, game_state):
        valid_moves = []
        for r in range(0, game_state.board._num_rows):
            for c in range(0, game_state.board._num_cols):
                p = Point(r, c)
                if game_state.is_valid_move_for_player(Move.play(p), game_state.next_player):
                    valid_moves.append(p)
        if not valid_moves:
            return Move.pass_turn()
        return Move.play(random.choice(valid_moves))