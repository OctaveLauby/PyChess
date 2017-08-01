from gameplay import InvalidMove
from parameters import BLACK, WHITE, TOP_COLOR
from pieces import (
    Bishop,
    Queen,
    King,
    Knight,
    Pawn,
    Rook,
)
from utils import Position


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


class PList(list):

    def deads_str(self):
        return (
            "["
            + " ".join([
                "-" if piece.is_alife() else piece.symbol()
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

        self._pieces = None
        self._playing_color = None
        self.init()

    def _add_piece(self, piece):
        self._board[piece.x][piece.y] = piece
        self._pieces[piece.color].append(piece)

    def init(self):
        """Initialize board pieces."""
        self._pieces = {
            BLACK: PList([]),
            WHITE: PList([]),
        }
        self._playing_color = WHITE
        for color in [BLACK, WHITE]:
            for pawn_n in range(8):
                x = 1 if color is TOP_COLOR else 6
                y = pawn_n
                pawn = Pawn(x, y, color)
                self._add_piece(pawn)

            lign = 0 if color is TOP_COLOR else 7
            self._add_piece(Bishop(lign, 2, color))
            self._add_piece(Bishop(lign, 5, color))
            self._add_piece(Knight(lign, 1, color))
            self._add_piece(Knight(lign, 6, color))
            self._add_piece(Rook(lign, 0, color))
            self._add_piece(Rook(lign, 7, color))
            if TOP_COLOR is BLACK:
                self._add_piece(Queen(lign, 3, color))
                self._add_piece(King(lign, 4, color))
            else:
                self._add_piece(King(lign, 3, color))
                self._add_piece(Queen(lign, 4, color))

    # ----------------------------------------------------------------------- #
    # Properties & g/s-etters

    @property
    def player(self):
        """Return current player color."""
        if self._playing_color is BLACK:
            return "Black"
        elif self._playing_color is WHITE:
            return "White"
        return None

    def get(self, position):
        """Return piece at position."""
        return self._board[position.x][position.y]

    def set(self, position, piece):
        """Set piece at position."""
        self._board[position.x][position.y] = piece

    # ----------------------------------------------------------------------- #
    # Playing

    def move(self, pos, npos):
        """Move piece at pos to npos if possible."""
        pos = Position(*pos)
        npos = Position(*npos)

        # Check square contains piece of right color
        piece = self.get(pos)
        if piece is None:
            raise InvalidMove("No piece on that position")
        elif piece.color is not self._playing_color:
            raise InvalidMove("You must move piece of your color")

        # Check whether move is possible
        move = piece.get_move(npos - pos)
        move.check(self)

        self._move(pos, npos, piece)

    def _move(self, pos, npos, piece):
        """Move piece with no checking."""
        # Kill future if exists
        npiece = self.get(npos)
        if npiece:
            npiece.kill()

        # Move piece
        piece.move(npos)
        self.set(pos, None)
        self.set(npos, piece)

        # New PLayer
        self._playing_color = BLACK if self._playing_color is WHITE else WHITE

    # ----------------------------------------------------------------------- #
    # Display

    def board_str(self):
        """Return board representation."""
        board = BOARD_FORMAT
        for x, y in Position.iter(8, 8):
            piece = self._board[x][y]
            r = " - " if (x + y) % 2 else "   "
            board = board.replace(
                "%s %s" % (x, y),
                repr(piece) if piece else r
            )
        return board

    def display(self):
        """Display board and killed pieces."""
        if TOP_COLOR is BLACK:
            top_color = "Black"
            bottom_color = "White"
        else:
            top_color = "White"
            bottom_color = "Black"

        print()
        print(top_color, ":", self._pieces[TOP_COLOR].deads_str())
        print(self.board_str())
        print(bottom_color, ":", self._pieces[1 - TOP_COLOR].deads_str())
