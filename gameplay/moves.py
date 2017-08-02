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
        board.set(cpos, None)
        board.set(npos, self.piece)

    def check(self, board):
        """Check whether move is possible."""
        cpos = self.get_origin()        # Current position
        npos = self.get_destination()   # Next position
        self.check_boundaries(npos, board)
        self.check_path(cpos, board)
        self.check_destination(npos, board)
        return True

    def check_boundaries(self, npos, board):
        """Check whether destination is within board."""
        if npos.x < 0 or npos.x > 7 or npos.y < 0 or npos.y > 7:
            raise InvalidMove("Moving piece out of boundaries")

    def check_destination(self, npos, board):
        """Check whether destination is accessible."""
        npiece = board.get(npos)
        if npiece and npiece.color is self.piece.color:
            raise InvalidMove("Moving on a piece of same color")
        return True

    def check_path(self, cpos, board):
        """Watch out for pieces along the ways."""
        for int_pos in self.direction.iter(cpos, self.steps-1):
            if board.get(int_pos):
                raise InvalidMove("Bump into someone at %s" % int_pos)
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


class Castling(Move):
    """Castling."""

    def __init__(self, piece, direction):
        assert piece.__class__.__name__ == "King"
        super().__init__(
            piece,
            direction=direction,
            steps=2,
        )
        self._corner = piece.origin
        self._dist_to_corner = 0
        while 0 < self._corner.y < 7:
            self._dist_to_corner += 1
            self._corner = self._corner + self.direction

    @property
    def corner(self):
        """Corner where a rook is expected."""
        return self._corner

    @property
    def dist_to_corner(self):
        return self._dist_to_corner

    def do(self, board):
        cpos = self.get_origin()
        npos = self.get_destination()

        # Move king
        board.set(cpos, None)
        board.set(npos, self.piece)

        # Move rook
        rook = board.get(self.corner)
        board.set(self.corner, None)
        print(npos - self.direction, rook, npos, self.direction)
        board.set(npos - self.direction, rook)

    def check(self, board):
        if self.piece.has_moved():
            raise InvalidMove("Can't castle when King has moved")
        super().check(board)

    def check_destination(self, npos, board):
        return True

    def check_path(self, cpos, board):
        for int_pos in self.direction.iter(cpos, self.dist_to_corner - 1):
            if board.get(int_pos):
                raise InvalidMove("Can't castle when a piece is along the way")
        corner_piece = board.get(self.corner)
        if (
            corner_piece is None
            or corner_piece.__class__.__name__ is not "Rook"
        ):
            raise InvalidMove("Castling must evolve a rook")
        if corner_piece.has_moved():
            raise InvalidMove("Can't castle with a rook that has moved")
        return True


class LCastling(Castling):
    """Castling on the left."""

    def __init__(self, piece):
        super().__init__(
            piece,
            direction=(0, -1),
        )


class RCastling(Castling):
    """Castling on the right."""

    def __init__(self, piece):
        super().__init__(
            piece,
            direction=(0, 1),
        )
