import itertools

from parameters import BLACK, WHITE, TOP_COLOR
from pieces import (
    InvalidMove,
    Bishop,
    Queen,
    King,
    Knight,
    Pawn,
    Rook,
)
from utils.vector import Vector


BOARD_FORMAT = (
    """
      a   b   c   d   e   f   g   h
    +---+---+---+---+---+---+---+---+
  8 |0 0|0 1|0 2|0 3|0 4|0 5|0 6|0 7| 8
    +---+---+---+---+---+---+---+---+
  7 |1 0|1 1|1 2|1 3|1 4|1 5|1 6|1 7| 7
    +---+---+---+---+---+---+---+---+
  6 |2 0|2 1|2 2|2 3|2 4|2 5|2 6|2 7| 6
    +---+---+---+---+---+---+---+---+
  5 |3 0|3 1|3 2|3 3|3 4|3 5|3 6|3 7| 5
    +---+---+---+---+---+---+---+---+
  4 |4 0|4 1|4 2|4 3|4 4|4 5|4 6|4 7| 4
    +---+---+---+---+---+---+---+---+
  3 |5 0|5 1|5 2|5 3|5 4|5 5|5 6|5 7| 3
    +---+---+---+---+---+---+---+---+
  2 |6 0|6 1|6 2|6 3|6 4|6 5|6 6|6 7| 2
    +---+---+---+---+---+---+---+---+
  1 |7 0|7 1|7 2|7 3|7 4|7 5|7 6|7 7| 1
    +---+---+---+---+---+---+---+---+
      a   b   c   d   e   f   g   h
    """
)

CELLS = list(itertools.product(range(8), range(8)))


class PList(list):

    def string(self):
        return (
            "["
            + " ".join([
                "-" if piece.alife else piece.symbol()
                for piece in self
            ])
            + "]"
        )


class Board(object):

    def __init__(self):
        self._shape = (8, 8)
        self._board = []
        for x in range(8):
            self._board.append([])
            for y in range(8):
                self._board[x].append(None)

        self._pieces = {
            BLACK: PList([]),
            WHITE: PList([]),
        }
        self._playing_color = None
        self.init()

    def add_piece(self, piece):
        self._board[piece.x][piece.y] = piece
        self._pieces[piece.color].append(piece)

    def init(self):
        self._playing_color = WHITE
        for color in [BLACK, WHITE]:
            for pawn_n in range(8):
                x = 1 if color is TOP_COLOR else 6
                y = pawn_n
                pawn = Pawn(x, y, color)
                self.add_piece(pawn)

            lign = 0 if color is TOP_COLOR else 7
            self.add_piece(Bishop(lign, 2, color))
            self.add_piece(Bishop(lign, 5, color))
            self.add_piece(Knight(lign, 1, color))
            self.add_piece(Knight(lign, 6, color))
            self.add_piece(Rook(lign, 0, color))
            self.add_piece(Rook(lign, 7, color))
            if TOP_COLOR is BLACK:
                self.add_piece(Queen(lign, 3, color))
                self.add_piece(King(lign, 4, color))
            else:
                self.add_piece(King(lign, 3, color))
                self.add_piece(Queen(lign, 4, color))

    # ----------------------------------------------------------------------- #
    # Properties

    @property
    def player(self):
        if self._playing_color is BLACK:
            return "Black"
        elif self._playing_color is WHITE:
            return "White"
        return None

    # ----------------------------------------------------------------------- #
    # Playing

    def move(self, pos, npos):
        pos = Vector(*pos)
        npos = Vector(*npos)
        x, y = pos
        nx, ny = npos

        piece = self._board[x][y]
        if piece is None:
            raise InvalidMove("No piece on that position")
        elif piece.color is not self._playing_color:
            raise InvalidMove("You must move piece of your color")

        if nx < 0 or nx > 7 or ny < 0 or ny > 7:
            raise InvalidMove("Moving piece out of boundaries")

        move = piece.get_move(npos-pos)

        # Make sure you don't bumb into someone when moving:
        int_pos = pos.copy()
        for step in range(move.steps-1):
            int_pos += move
            ix, iy = int_pos
            if self._board[ix][iy]:
                raise InvalidMove("Bump into someone at (%s, %s)" % (ix, iy))
        # Check future
        npiece = self._board[nx][ny]
        if npiece:
            if npiece.color is self._playing_color:
                raise InvalidMove("Moving on a piece of your own")
            elif not move.can_kill:
                raise InvalidMove("Can't take a piece with this move")
        elif move.must_kill:
            raise InvalidMove("This move is valid only if it kills a piece")

        self._move(x, y, nx, ny, piece)

    def _move(self, x, y, nx, ny, piece):
        self._board[x][y] = None
        npiece = self._board[nx][ny]
        if npiece:
            npiece.kill()
        piece.pos = (nx, ny)
        self._board[nx][ny] = piece
        self._playing_color = BLACK if self._playing_color is WHITE else WHITE

    # ----------------------------------------------------------------------- #
    # Display

    def board_str(self):
        board = BOARD_FORMAT
        for x, y in CELLS:
            piece = self._board[x][y]
            r = " - " if (x + y) % 2 else "   "
            board = board.replace(
                "%s %s" % (x, y),
                repr(piece) if piece else r
            )
        return board

    def display(self):
        if TOP_COLOR is BLACK:
            top_color = "Black"
            bottom_color = "White"
        else:
            top_color = "White"
            bottom_color = "Black"

        print()
        print(top_color, ":", self._pieces[TOP_COLOR].string())
        print(self.board_str())
        print(bottom_color, ":", self._pieces[1 - TOP_COLOR].string())
