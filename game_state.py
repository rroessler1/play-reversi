from __future__ import annotations
import copy
from board import Board
from reversi_types import Move, Player, Point
from typing import Dict, Optional


class GameState:
    def __init__(self, board: Board, next_player: Player, previous_game_state: GameState, move: Move):
        self.board: Board = board
        self.next_player: Player = next_player
        self._previous_game_state: GameState = previous_game_state
        self.move: Move = move

    def apply_move(self, move: Move) -> GameState:
        if not move.is_pass:
            # TODO: I don't think this should be needed, and I bet it slows it down a lot
            next_board = copy.deepcopy(self.board)
            # TODO: let's do validation if this is valid, if that's the Pythonic way
            next_board.place_piece(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    def get_result(self) -> Dict[Player, int]:
        res: Dict[Player, int] = {}
        for key, value in self.board._grid.items():
            if res.get(value) is None:
                res[value] = 1
            else:
                res[value] += 1
        return res

    def get_winner(self) -> Optional[Player]:
        res = self.get_result()
        if res.get(Player.white) > res.get(Player.black):
            return Player.white
        elif res.get(Player.black) > res.get(Player.white):
            return Player.black
        else:
            return None

    def is_over(self) -> bool:
        return self._previous_game_state and self._previous_game_state.move and \
               self._previous_game_state.move.is_pass and self.move.is_pass

    def is_valid_move_for_player(self, move: Move, player: Player) -> bool:
        if self.is_over():
            return False
        # TODO: this isn't correct, is_pass is only valid if there are no other moves available
        #       but we're actually validating elsewhere so it's ok
        if move.is_pass:
            return True
        return self.board.is_valid_move_for_player(move, player)

    @classmethod
    def new_game(cls, board_size: int) -> GameState:
        board = Board(board_size, board_size)
        # these can be None for initial state only
        # noinspection PyTypeChecker
        return GameState(board, Player.black, None, None)

    @staticmethod
    def corner_evaluation_function(game_state: GameState) -> int:
        corners = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        res = {Player.white: 0, Player.black: 0}
        for corner in corners:
            if game_state.board._grid.get(corner):
                res[game_state.board._grid.get(corner)] += 50
        return res[Player.white] - res[Player.black]

    @staticmethod
    def piece_count_evaluation_function(game_state: GameState) -> int:
        piece_count = game_state.get_result()
        return piece_count[Player.white] - piece_count[Player.black]
