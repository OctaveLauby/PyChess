from .piece import Piece
from gameplay.moves import Move


class Knight(Piece):

    def init_moves(self):
        self._can_cross = True
        self._moves = [
            Move(self, (+2, +1)),
            Move(self, (+2, -1)),
            Move(self, (-2, +1)),
            Move(self, (-2, -1)),
            Move(self, (+1, +2)),
            Move(self, (+1, -2)),
            Move(self, (-1, +2)),
            Move(self, (-1, -2)),
        ]

    def symbol(self):
        return "N"
