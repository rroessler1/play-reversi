from __future__ import annotations
from typing import List, NamedTuple, Optional
import enum


class Player(enum.Enum):
    none = 0
    black = 1
    white = 2

    @property
    def other(self) -> Player:
        return Player.black if self == Player.white else Player.white


class Point(NamedTuple):
    row: int
    col: int

    def neighbors(self) -> List[Point]:
        return [
            Point(self.row - 1, self.col - 1),
            Point(self.row, self.col - 1),
            Point(self.row + 1, self.col - 1),
            Point(self.row - 1, self.col),
            Point(self.row + 1, self.col),
            Point(self.row - 1, self.col + 1),
            Point(self.row, self.col + 1),
            Point(self.row + 1, self.col + 1),
        ]

    def get_neighbor(self, x, y) -> Point:
        return Point(self.row + x, self.col + y)


class Shift(NamedTuple):
    x: int
    y: int

    @staticmethod
    def shifts() -> List[Shift]:
        return [
            Shift(-1, -1),
            Shift(0, -1),
            Shift(1, -1),
            Shift(-1, 0),
            Shift(1, 0),
            Shift(-1, 1),
            Shift(0, 1),
            Shift(1, 1),
        ]


class Move(NamedTuple):
    point: Optional[Point]
    is_pass: bool = False

    @classmethod
    def play(cls, point) -> Move:
        return Move(point)

    @classmethod
    def pass_turn(cls) -> Move:
        return Move(None, True)
