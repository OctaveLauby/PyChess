from .piece import InvalidMove, Piece
from .move import Move


class Pawn(Piece):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._or_pos = self.pos.copy()

    def init_moves(self):
        self._special_move = Move(self.dir * (2, 0), can_kill=False)
        self._moves = [
            Move(self.dir * (1, 0), can_kill=False),
            Move(self.dir * (1, 1), must_kill=True),
            Move(self.dir * (1, -1), must_kill=True),
            self._special_move,
        ]

    def get_move(self, *args, **kwargs):
        move = super().get_move(*args, **kwargs)
        if move == self._special_move and self._or_pos != self.pos:
            raise InvalidMove("Pawn can't jump when moved already")
        return move

    def symbol(self):
        return "P"
