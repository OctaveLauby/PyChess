import itertools

from .piece import Piece
from gameplay.moves import Move


class King(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if dpos == (0, 0):
                continue
            self._moves.append(Move(self, dpos))

    def symbol(self):
        return "K"
