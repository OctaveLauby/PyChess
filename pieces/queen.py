import itertools

from .piece import Piece
from .move import Move


class Queen(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if dpos == (0, 0):
                continue
            for scal in range(1, 8):
                self._moves.append(Move(dpos, steps=scal))

    def symbol(self):
        return "Q"
