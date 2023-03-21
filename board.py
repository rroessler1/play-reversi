from __future__ import annotations
from reversi_types import Player, Point, Shift
from typing import Dict, Set


class IllegalMoveException(Exception):
    pass


class Board:
    def __init__(self, num_rows: int, num_cols: int):
        self._num_rows: int = num_rows
        self._num_cols: int = num_cols
        self._possibly_valid_points: Set[Point] = set()
        self._grid: Dict[Point, Player] = {}
        self._set_initial_board_state()

    def _set_initial_board_state(self) -> None:
        self._grid[Point(3, 3)] = Player.white
        self._grid[Point(3, 4)] = Player.black
        self._grid[Point(4, 3)] = Player.black
        self._grid[Point(4, 4)] = Player.white
        self._add_adjacent_points_as_possible_points(Point(3, 3))
        self._add_adjacent_points_as_possible_points(Point(3, 4))
        self._add_adjacent_points_as_possible_points(Point(4, 3))
        self._add_adjacent_points_as_possible_points(Point(4, 4))

    def place_piece(self, player: Player, point: Point) -> None:
        if not self._point_is_open(point):
            raise IllegalMoveException("That is not a valid square to place a piece.")
        flipped_something = False
        for shift in Shift.shifts():
            neighbor = point.get_neighbor(shift.x, shift.y)
            did_flip = self.maybe_flip(neighbor, player, shift, do_flip=True)
            flipped_something = flipped_something or did_flip
        if not flipped_something:
            raise IllegalMoveException("That is not a valid move, as it won't flip any pieces.")
        self._grid[point] = player
        self._add_adjacent_points_as_possible_points(point)
        self._possibly_valid_points.remove(point)

    def _add_adjacent_points_as_possible_points(self, played_point: Point) -> None:
        for shift in Shift.shifts():
            neighbor = played_point.get_neighbor(shift.x, shift.y)
            if self.is_on_grid(neighbor) and not self._grid.get(neighbor):
                self._possibly_valid_points.add(neighbor)

    def get(self, point: Point) -> Player:
        return self._grid.get(point)

    def is_on_grid(self, point: Point) -> bool:
        return 0 <= point.row < self._num_rows and 0 <= point.col < self._num_cols

    def _point_is_open(self, point: Point) -> bool:
        return self.is_on_grid(point) and self.get(point) is None

    def maybe_flip(self, point: Point, current_player: Player, shift: Shift, do_flip: bool = True) -> bool:
        """
        Traverses in a direction, and flips everything in between if we eventually find a stone of the current player's
        color.
        :param point: The current point to flip.
        :param current_player: The current player, therefore, the color stone we are looking for.
        :param shift: The direction we are going.
        :param do_flip: If we should actually flip the disks on the board.
        :return: True if something was flipped.  We can be greedy because as long as something is flipped,
        the move will be valid.
        """
        if not self._point_is_open(point):
            return False
        if self._grid.get(point) == current_player:
            return False
        # TODO: should this function handle the shifting itself?  The board should know how to shift
        neighbor = point.get_neighbor(shift.x, shift.y)
        flipped_neighbor = self.maybe_flip(neighbor, current_player, shift, do_flip)
        if flipped_neighbor or self._grid.get(neighbor) == current_player:
            if do_flip:
                self._grid[point] = current_player
            return True
        return False

    def is_valid_point_to_play(self, point: Point, player: Player) -> bool:
        if not self._point_is_open(point):
            return False
        for shift in Shift.shifts():
            neighbor = point.get_neighbor(shift.x, shift.y)
            if self.maybe_flip(neighbor, player, shift, do_flip=False):
                return True
        return False

    def get_result(self) -> Dict[Player, int]:
        res: Dict[Player, int] = {}
        for key, value in self._grid.items():
            if res.get(value) is None:
                res[value] = 1
            else:
                res[value] += 1
        return res

    @staticmethod
    def corner_evaluation_function(board: Board) -> int:
        corners = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        res = {Player.white: 0, Player.black: 0}
        for corner in corners:
            if board._grid.get(corner):
                res[board._grid.get(corner)] += 50
        return res[Player.white] - res[Player.black]

    @staticmethod
    def piece_count_evaluation_function(board: Board) -> int:
        piece_count = board.get_result()
        return piece_count[Player.white] - piece_count[Player.black]
