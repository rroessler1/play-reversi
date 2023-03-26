import math

from agent.base import Agent
from game_state import GameState
from monte_carlo_node import MonteCarloNode
from reversi_types import Move


class MctAgent(Agent):
    def __init__(self):
        super().__init__()
        self._num_rounds = 500
        self._temperature = 1.5

    def select_move(self, game_state: GameState) -> Move:
        root = MonteCarloNode(game_state)

        for i in range(self._num_rounds):
            if i % 100 == 0:
                print(i)
            node = root
            while (not node.is_terminal()) and (not node.can_add_child()):
                node = self.select_child(node)
            if node.can_add_child():
                node = node.add_random_child()
            winner = node.simulate_random_game()
            while node is not None:
                node.record_win(winner)
                node = node.parent

        best_child: MonteCarloNode = root.children[0]
        for child in root.children:
            if child.winning_fraction(game_state.next_player) > best_child.winning_fraction(game_state.next_player):
                best_child = child
        return best_child.move

    def select_child(self, node: MonteCarloNode) -> MonteCarloNode:
        max_score = -1
        best_child = None
        for child in node.children:
            score = uct_score(node.num_rollouts, child.num_rollouts, child.winning_fraction(node.game_state.next_player), self._temperature)
            if score > max_score:
                max_score = score
                best_child = child
        return best_child


def uct_score(parent_rollouts, child_rollouts, win_percentage, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_percentage + temperature * exploration
