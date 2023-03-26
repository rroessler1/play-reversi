from board import Board
from reversi_types import Move, Player, Point


COLS = 'ABCDEFGH'
PIECE_TO_CHAR = {
    None: " . ",
    Player.black: ' X ',
    Player.white: ' O ',
}


class MalformedMoveCoordinatesException(Exception):
    pass


def move_from_coordinates(coords_string: str) -> Move:
    if coords_string.lower().strip() == "pass":
        return Move.pass_turn()
    if len(coords_string) != 2 or coords_string[0] not in COLS or coords_string[1] < '0' or coords_string[1] > '7':
        raise MalformedMoveCoordinatesException(f"%s is not a valid coordinate string." % coords_string)
    col = COLS.index(coords_string[0])
    row = int(coords_string[1])
    return Move.play(Point(row, col))


def print_move(player: Player, move: Move) -> None:
    move_str = "passes" if move.is_pass else '%s%d' % (COLS[move.point.col], move.point.row)
    print('%s %s' % (player, move_str))


def print_board(board: Board) -> None:
    print("    " + "  ".join([c for c in COLS]))
    for r in range(board._num_rows):
        row_str = "".join([PIECE_TO_CHAR[board.get_player_at_point(Point(r, c))] for c in range(board._num_cols)])
        print(" " + str(r) + " " + row_str)
    valid_moves = [("%s%s " % (COLS[p.col], p.row)) for p in board._adjacent_unoccupied_points]
    valid_moves.sort()
    print(" ".join(valid_moves))
