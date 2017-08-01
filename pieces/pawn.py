from .piece import Piece
from gameplay import InvalidMove, Move
from utils import Vector


class Pawn(Piece):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._or_pos = self.pos.copy()

    def init_moves(self):
        self._special_move = Move(
            self.dir * Vector(1, 0),
            steps=2,
            can_kill=False
        )
        self._moves = [
            Move(self.dir * Vector(1, 0), can_kill=False),
            Move(self.dir * Vector(1, 1), must_kill=True),
            Move(self.dir * Vector(1, -1), must_kill=True),
            self._special_move,
        ]

    def get_move(self, *args, **kwargs):
        move = super().get_move(*args, **kwargs)
        if move == self._special_move and self.has_moved():
            raise InvalidMove("Pawn can't jump when moved already")
        return move

    def symbol(self):
        return "P"
