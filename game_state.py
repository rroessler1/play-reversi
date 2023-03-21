from __future__ import annotations
import copy
from board import Board
from reversi_types import Move, Player
from typing import Dict, Optional, Iterator


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
            next_board.place_piece(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    def get_all_valid_moves(self) -> Iterator[Move]:
        valid_points = list(self.board.get_all_valid_points_to_play(self.next_player))
        if len(valid_points) == 0:
            return Move.pass_turn()
        else:
            return map(lambda p: Move.play(p), valid_points)

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
        return self.board.is_valid_point_to_play(move.point, player)

    def get_result(self) -> Dict[Player, int]:
        return self.board.get_result()

    @classmethod
    def new_game(cls, board_size: int) -> GameState:
        board = Board(board_size, board_size)
        # these can be None for initial state only
        # noinspection PyTypeChecker
        return GameState(board, Player.black, None, None)
