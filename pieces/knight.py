from .piece import Piece
from .move import Move


class Knight(Piece):

    def init_moves(self):
        self._can_cross = True
        self._moves = [
            Move((+2, +1)),
            Move((+2, -1)),
            Move((-2, +1)),
            Move((-2, -1)),
            Move((+1, +2)),
            Move((+1, -2)),
            Move((-1, +2)),
            Move((-1, -2)),
        ]

    def symbol(self):
        return "N"
