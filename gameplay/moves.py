from utils import Vector

from .errors import InvalidMove


class Move(object):
    """Basic move.

    A piece, a direction and a number of steps.
    """

    def __init__(self, piece, direction, steps=1):
        self._dir = Vector(direction)
        self._piece = piece
        self._steps = steps
        self._vector = self._dir * self.steps

    # Utils

    @property
    def direction(self):
        return self._dir

    @property
    def piece(self):
        return self._piece

    @property
    def steps(self):
        return self._steps

    @property
    def vector(self):
        return self._vector

    def get_destination(self):
        """Destination position of piece."""
        return self.piece.pos + self.vector

    def get_origin(self):
        """Current position of piece."""
        return self.piece.pos

    def __eq__(self, other):
        return self.vector == other

    def __str__(self):
        return super().__str__() + "%s>" % self.steps

    # Action

    def do(self, board):
        """Move piece with no checking."""
        # Kill future if exists
        cpos = self.get_origin()
        npos = self.get_destination()
        npiece = board.get(npos)
        if npiece:
            npiece.kill()

        # Move piece
        self.piece.move(npos)
        board.set(cpos, None)
        board.set(npos, self.piece)

    def check(self, board):
        """Check whether move is possible."""
        cpos = self.get_origin()        # Current position
        npos = self.get_destination()   # Next position

        # Check future
        # ---- boundaries
        if npos.x < 0 or npos.x > 7 or npos.y < 0 or npos.y > 7:
            raise InvalidMove("Moving piece out of boundaries")

        # ---- Watch out for pieces along the way
        int_pos = cpos.copy()
        for step in range(self.steps-1):
            int_pos = int_pos + self.direction
            if board.get(int_pos):
                raise InvalidMove("Bump into someone at %s" % int_pos)

        self.check_destination(npos, board)
        return True

    def check_destination(self, npos, board):
        """Check whether destination is accessible."""
        npiece = board.get(npos)
        if npiece and npiece.color is self.piece.color:
            raise InvalidMove("Moving on a piece of same color")
        return True


class CaptureMove(Move):
    """A move that must capture an enemy piece."""

    def check_destination(self, npos, board):
        """Check whether there is an enemy at destination."""
        npiece = board.get(npos)
        if npiece is None or npiece.color is self.piece.color:
                raise InvalidMove("Must capture a piece with that move")
        return True


class PeaceMove(Move):
    """A move that must reach an empty square."""

    def check_destination(self, npos, board):
        """Check whether there is an enemy at destination."""
        npiece = board.get(npos)
        if npiece is not None:
            raise InvalidMove("Can't move on another piece with that move")
        return True


class FirstMove(PeaceMove):
    """First move of a piece. Must be peaceful."""

    def check(self, board):
        if self.piece.has_moved():
            raise InvalidMove("Forbidden when piece has moved already")
        super().check(board)
