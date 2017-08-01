from parameters import BLACK, WHITE, TOP_COLOR
from utils import Position, Vector


class InvalidMove(Exception):
    pass


class Piece(object):

    def __init__(self, x, y, color):
        self._alife = True
        self._color = color
        self._direction = (
            Vector(1, 1) if self._color is TOP_COLOR else Vector(-1, 1)
        )

        self._pos = Position(x, y)
        self._or_pos = Position(x, y)
        self._has_moved = False

        self._moves = None
        self.init_moves()

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
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    def is_alife(self):
        return self._alife

    def color_name(self):
        if self.color is BLACK:
            return "black"
        elif self.color is WHITE:
            return "white"

    def get_move(self, move_tuple):
        for move in self._moves:
            if move == move_tuple:
                return move
        raise InvalidMove(
            "%s %s can't do %s move."
            % (self.color_name(), self.__class__.__name__, move_tuple)
        )

    def has_moved(self):
        return self._has_moved

    def kill(self):
        self._alife = False

    def move(self, npos):
        """Go not next position."""
        self._has_moved = True
        self._pos = Position(npos)

    def symbol(self):
        return "?"

    def __repr__(self):
        ind = "?"
        if self.color is WHITE:
            ind = "w"
        elif self.color is BLACK:
            ind = "b"
        return ind + self.symbol() + ind

    def __string__(self):
        return "{} {}".format(self.symbol(), self.pos)
