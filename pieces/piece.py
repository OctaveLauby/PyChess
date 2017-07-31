from parameters import BLACK, WHITE
from utils.vector import Vector


class InvalidMove(Exception):
    pass


class Piece(object):

    def __init__(self, x, y, color):
        self._alife = True
        self._color = color
        self._direction = (
            Vector(1, 1) if self._color is BLACK else Vector(-1, 1)
        )
        self._pos = Vector(x, y)

        self._moves = None
        self._can_cross = False
        self.init_moves()

    def init_moves(self):
        raise NotImplementedError

    @property
    def alife(self):
        return self._alife

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

    @pos.setter
    def pos(self, npos):
        """Go not next position."""
        self._pos = Vector(npos[0], npos[1])

    def kill(self):
        self._alife = False

    def get_move(self, move_tuple):
        for move in self._moves:
            if move == move_tuple:
                return move
        raise InvalidMove(
            "%s can't do %s move."
            % (self.__class__.__name__, move_tuple)
        )

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
        return "{} ({}, {})".format(self.symbol(), *self.pos)
