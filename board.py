import copy
from collections import namedtuple
from reversi_types import Player, Point


class IllegalMoveException(Exception):
    pass


class Board:
    def __init__(self, num_rows, num_cols):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.possibly_valid_points = set()
        self._grid = {}
        self.set_initial_reversi_state()

    def set_initial_reversi_state(self):
        self._grid[Point(3, 3)] = Player.white
        self._grid[Point(3, 4)] = Player.black
        self._grid[Point(4, 3)] = Player.black
        self._grid[Point(4, 4)] = Player.white
        self.add_adjacent_points_as_possible_moves(Point(3, 3))
        self.add_adjacent_points_as_possible_moves(Point(3, 4))
        self.add_adjacent_points_as_possible_moves(Point(4, 3))
        self.add_adjacent_points_as_possible_moves(Point(4, 4))

    def place_piece(self, player, point):
        if not self.can_place_piece(point):
            raise IllegalMoveException("That is not a valid square to place a piece.")
        flipped_something = False
        for shift in Shift.shifts():
            neighbor = point.get_neighbor(shift.x, shift.y)
            did_flip = self.maybe_flip(neighbor, player, shift, do_flip=True)
            flipped_something = flipped_something or did_flip
        if not flipped_something:
            raise IllegalMoveException("That is not a valid move, as it won't flip any pieces.")
        self._grid[point] = player
        self.add_adjacent_points_as_possible_moves(point)
        self.possibly_valid_points.remove(point)

    def add_adjacent_points_as_possible_moves(self, played_point):
        for shift in Shift.shifts():
            neighbor = played_point.get_neighbor(shift.x, shift.y)
            if self.is_on_grid(neighbor) and not self._grid.get(neighbor):
                self.possibly_valid_points.add(neighbor)

    def get(self, point):
        return self._grid.get(point)

    def is_on_grid(self, point):
        return 0 <= point.row < self.num_rows and 0 <= point.col < self.num_cols

    def can_place_piece(self, point):
        return self.is_on_grid(point) and self._grid.get(point) is None

    def maybe_flip(self, point, current_player, shift, do_flip=True):
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
        if not self.is_on_grid(point):
            return False
        if self._grid.get(point) is None:
            return False
        if self._grid.get(point) == current_player:
            return False
        neighbor = point.get_neighbor(shift.x, shift.y)
        flipped_neighbor = self.maybe_flip(neighbor, current_player, shift, do_flip)
        if flipped_neighbor or self._grid.get(neighbor) == current_player:
            if do_flip:
                self._grid[point] = current_player
            return True
        return False

    def is_valid_move_for_player(self, move, player):
        if not self.can_place_piece(move.point):
            return False
        for shift in Shift.shifts():
            neighbor = move.point.get_neighbor(shift.x, shift.y)
            if self.maybe_flip(neighbor, player, shift, do_flip=False):
                return True
        return False

    def get_all_valid_moves(self, player):
        valid_moves = set()
        for move in self.possibly_valid_points:
            if self.is_valid_move_for_player(move, player):
                valid_moves.add(move)
        return valid_moves


class GameState:
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous = previous
        self.move = move

    def apply_move(self, move):
        if not move.is_pass:
            next_board = copy.deepcopy(self.board)
            next_board.place_piece(self.next_player, move.point)
        else:
            next_board = self.board
        return GameState(next_board, self.next_player.other, self, move)

    def get_result(self):
        res = {}
        for key, value in self.board._grid.items():
            if res.get(value) is None:
                res[value] = 1
            else:
                res[value] += 1
        return res

    def get_winner(self):
        res = self.get_result()
        if res.get(Player.white) > res.get(Player.black):
            return Player.white
        elif res.get(Player.black) > res.get(Player.white):
            return Player.black
        else:
            return None

    def is_over(self):
        return self.previous and self.previous.move and self.previous.move.is_pass and self.move.is_pass

    def is_valid_move_for_player(self, move, player):
        if self.is_over():
            return False
        if move.is_pass:
            return True
        return self.board.is_valid_move_for_player(move, player)

    @classmethod
    def new_game(cls, board_size):
        board = Board(board_size, board_size)
        return GameState(board, Player.black, None, None)

    @staticmethod
    def corner_evaluation_function(game_state):
        corners = [Point(0, 0), Point(0, 7), Point(7, 0), Point(7, 7)]
        res = {Player.white: 0, Player.black: 0}
        for corner in corners:
            if game_state.board._grid.get(corner):
                res[game_state.board._grid.get(corner)] += 50
        return res[Player.white] - res[Player.black]

    @staticmethod
    def piece_count_evaluation_function(game_state):
        piece_count = game_state.get_result()
        return piece_count[Player.white] - piece_count[Player.black]
