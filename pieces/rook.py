from .piece import Piece
from gameplay.move import Move


class Rook(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in [(+1, 0), (0, -1), (0, +1), (-1, 0)]:
            for scal in range(1, 8):
                self._moves.append(Move(dpos, steps=scal))

    def symbol(self):
        return "R"
