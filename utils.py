import reversi_types


COLS = 'ABCDEFGH'
PIECE_TO_CHAR = {
    None: " . ",
    reversi_types.Player.black: ' X ',
    reversi_types.Player.white: ' O ',
}


def move_from_coordinates(coords_string):
    col = COLS.index(coords_string[0])
    row = int(coords_string[1])
    return reversi_types.Point(row, col)


def print_move(player, move):
    move_str = "passes" if move.is_pass else '%s%d' % (COLS[move.point.col], move.point.row)
    print('%s %s' % (player, move_str))


def print_board(board):
    print("    " + "  ".join([c for c in COLS]))
    for r in range(board.num_rows):
        row_str = "".join([PIECE_TO_CHAR[board._grid.get(reversi_types.Point(r, c))] for c in range(board.num_cols)])
        print(" " + str(r) + " " + row_str)
    valid_moves = [("%s%s " % (COLS[p.col], p.row)) for p in board._possibly_valid_points]
    valid_moves.sort()
    print(" ".join(valid_moves))
