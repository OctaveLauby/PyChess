from .piece import Piece
from gameplay.moves import Move


class Bishop(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in [(+1, +1), (+1, -1), (-1, +1), (-1, -1)]:
            for scal in range(1, 8):
                self._moves.append(Move(self, dpos, steps=scal))

    def symbol(self):
        return "B"
