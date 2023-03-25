from __future__ import annotations
from game_state import GameState
from reversi_types import Move, Player
from typing import Dict, List

import random


class MonteCarloNode(object):
    def __init__(self, game_state: GameState, parent: MonteCarloNode = None, move: Move = None):
        self.game_state: GameState = game_state
        self.parent: MonteCarloNode = parent
        self.move: Move = move
        self.win_counts: Dict[Player, int] = {
            Player.black: 0,
            Player.white: 0,
        }
        self.num_rollouts: int = 0
        self.children: List[MonteCarloNode] = []
        self.unvisited_moves: List[Move] = list(game_state.get_all_valid_moves())

    def add_random_child(self) -> MonteCarloNode:
        idx = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(idx)
        new_game_state = self.game_state.apply_move(new_move)
        new_node = MonteCarloNode(new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node

    def record_win(self, winner: Player) -> None:
        self.win_counts[winner] += 1
        self.num_rollouts += 1

    def can_add_child(self) -> bool:
        return len(self.unvisited_moves) > 0

    def is_terminal(self) -> bool:
        return self.game_state.is_over()

    def winning_fraction(self, player: Player) -> float:
        return float(self.win_counts[player])/float(self.num_rollouts)
