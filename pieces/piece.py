from gameplay import InvalidMove
from parameters import BLACK, WHITE, TOP_COLOR
from utils import Position, Vector


class Piece(object):

    pieces = {
        BLACK: [],
        WHITE: []
    }
    count = 0

    def __init__(self, x, y, color):
        self._alife = True
        self._color = color
        self._direction = (
            Vector(1, 1) if self._color is TOP_COLOR else Vector(-1, 1)
        )

        self._pos = Position(x, y)
        self._or_pos = Position(x, y)
        self._moves_n = 0

        self._moves = None
        self.init_moves()

        Piece.count += 1
        self._id = Piece.count
        Piece.pieces[color].append(self)

    def init_moves(self):
        raise NotImplementedError

    @property
    def color(self):
        return self._color

    @property
    def dir(self):
        return self._direction

    @property
    def pos(self):
        return self._pos

    @property
    def origin(self):
        return self._or_pos

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    def set(self, npos):
        """Go not next position."""
        self._moves_n += 1
        self._pos = Position(npos)

    def unset(self, opos):
        self._moves_n -= 1
        self._pos = Position(opos)

    # Utils

    def is_alife(self):
        """Whether piece is still active."""
        return self._alife

    def color_name(self):
        """Color name of piece."""
        if self.color is BLACK:
            return "black"
        elif self.color is WHITE:
            return "white"

    def get_move(self, move_tuple):
        """Return move if exists, raise InvalidMove if not."""
        for move in self._moves:
            if move == move_tuple:
                return move
        raise InvalidMove(
            "%s %s can't do %s move."
            % (self.color_name(), self.__class__.__name__, move_tuple)
        )

    def has_moved(self):
        return self._moves_n > 0

    def kill(self):
        self._alife = False

    def symbol(self):
        return "?"

    def unkill(self):
        self._alife = True

    def repr(self):
        ind = "?"
        if self.color is WHITE:
            ind = "w"
        elif self.color is BLACK:
            ind = "b"
        return ind + self.symbol() + ind

    def __repr__(self):
        return "<{} {} {}>".format(
            self.color_name(),
            self.__class__.__name__,
            self.pos,
        )

    def __str__(self):
        return self.__repr__()
