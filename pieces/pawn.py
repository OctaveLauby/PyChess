from gameplay.moves import CaptureMove, FirstMove, PeaceMove
from utils import Vector

from .piece import Piece


class Pawn(Piece):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_moves(self):
        self._moves = [
            PeaceMove(self, self.dir * Vector(1, 0)),
            CaptureMove(self, self.dir * Vector(1, 1)),
            CaptureMove(self, self.dir * Vector(1, -1)),
            FirstMove(self, self.dir * Vector(1, 0), steps=2)
        ]

    def symbol(self):
        return "P"
