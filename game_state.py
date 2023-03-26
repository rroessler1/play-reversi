from __future__ import annotations
from board import Board, IllegalMoveException
from reversi_types import Move, Player
from typing import Dict, Optional, List


class GameState:
    def __init__(self, board: Board, next_player: Player, move: Move):
        self.board: Board = board
        self.next_player: Player = next_player
        self._previous_move: Move = Move.pass_turn()
        self.move: Move = move

    def apply_move(self, move: Move) -> None:
        if not move.is_pass:
            self.board.place_piece(self.next_player, move.point)
        elif not self._can_pass():
            raise IllegalMoveException(
                f"You have some valid moves are are not allowed to pass.\n"
                f"Valid moves: {list(self.board.get_all_valid_points_to_play(self.next_player))}")
        self._previous_move = self.move
        self.move = move
        self.next_player = self.next_player.other

    def _can_pass(self) -> bool:
        return len(list(self.board.get_all_valid_points_to_play(self.next_player))) == 0

    def get_all_valid_moves(self) -> List[Move]:
        valid_points = list(self.board.get_all_valid_points_to_play(self.next_player))
        if len(valid_points) == 0:
            return [Move.pass_turn()]
        else:
            return [Move.play(p) for p in valid_points]

    def get_winner(self) -> Optional[Player]:
        res = self.get_result()
        if res.get(Player.white) > res.get(Player.black):
            return Player.white
        elif res.get(Player.black) > res.get(Player.white):
            return Player.black
        else:
            return None

    def is_over(self) -> bool:
        return self._previous_move.is_pass and self.move.is_pass

    def is_valid_move_for_player(self, move: Move, player: Player) -> bool:
        if self.is_over():
            return move.is_pass
        if move.is_pass:
            return self._can_pass()
        return self.board.is_valid_point_to_play(move.point, player)

    def get_result(self) -> Dict[Player, int]:
        return self.board.get_result()

    @classmethod
    def new_game(cls, board_size: int) -> GameState:
        board = Board(board_size, board_size)
        # these can be None for initial state only
        # noinspection PyTypeChecker
        return GameState(board, Player.black, None)
