import itertools
BLACK = 0
WHITE = 1


BOARD_FORMAT = (
    """
      a   b   c   d   e   f   g   h
    +---+---+---+---+---+---+---+---+
  8 |0 0|0 1|0 2|0 3|0 4|0 5|0 6|0 7| 8
    +---+---+---+---+---+---+---+---+
  7 |1 0|1 1|1 2|1 3|1 4|1 5|1 6|1 7| 7
    +---+---+---+---+---+---+---+---+
  6 |2 0|2 1|2 2|2 3|2 4|2 5|2 6|2 7| 6
    +---+---+---+---+---+---+---+---+
  5 |3 0|3 1|3 2|3 3|3 4|3 5|3 6|3 7| 5
    +---+---+---+---+---+---+---+---+
  4 |4 0|4 1|4 2|4 3|4 4|4 5|4 6|4 7| 4
    +---+---+---+---+---+---+---+---+
  3 |5 0|5 1|5 2|5 3|5 4|5 5|5 6|5 7| 3
    +---+---+---+---+---+---+---+---+
  2 |6 0|6 1|6 2|6 3|6 4|6 5|6 6|6 7| 2
    +---+---+---+---+---+---+---+---+
  1 |7 0|7 1|7 2|7 3|7 4|7 5|7 6|7 7| 1
    +---+---+---+---+---+---+---+---+
      a   b   c   d   e   f   g   h
    """
)

CELLS = list(itertools.product(range(8), range(8)))


class InvalidMove(Exception):
    pass


class Vector(list):
    def __init__(self, x, y):
        super().__init__((x, y))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    def copy(self):
        return Vector(self.x, self.y)

    def __add__(self, vector):
        return Vector(self.x + vector[0], self.y + vector[1])

    def __radd__(self, vector):
        return self + vector

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(other*self.x, other*self.y)
        return Vector(self.x*other[0], self.y*other[1])

    def __rmul__(self, vector):
        return self * vector

    def __sub__(self, vector):
        return Vector(self.x - vector[0], self.y - vector[1])

    def __eq__(self, other):
        return (self.x, self.y) == (other[0], other[1])


class Move(Vector):
    def __init__(self, dir, steps=1, can_kill=True, must_kill=False):
        super().__init__(*dir)
        self._must_kill = must_kill
        self._can_kill = can_kill
        self._steps = steps

    @property
    def can_kill(self):
        return self._can_kill

    @property
    def must_kill(self):
        return self._must_kill

    @property
    def steps(self):
        return self._steps

    def match(self, dpos):
        return self == dpos

    def __eq__(self, other):
        return Vector(self.x, self.y) * self.steps == (other[0], other[1])

    def __str__(self):
        return super().__str__() + "%s>" % self.steps


class Board(object):

    def __init__(self):
        self._shape = (8, 8)
        self._board = []
        for x in range(8):
            self._board.append([])
            for y in range(8):
                self._board[x].append(None)

        self._pieces = []
        self._playing_color = None
        self.init()

    def init(self):
        self._playing_color = WHITE
        for color in [BLACK, WHITE]:
            for pawn_n in range(8):
                x = 1 if color is BLACK else 6
                y = pawn_n
                pawn = Pawn(x, y, color)
                self.add_piece(pawn)

            lign = 0 if color is BLACK else 7
            self.add_piece(Bishop(lign, 2, color))
            self.add_piece(Bishop(lign, 5, color))
            self.add_piece(Knight(lign, 1, color))
            self.add_piece(Knight(lign, 6, color))
            self.add_piece(Rook(lign, 0, color))
            self.add_piece(Rook(lign, 7, color))
            self.add_piece(Queen(lign, 3, color))
            self.add_piece(King(lign, 4, color))

    @property
    def player(self):
        if self._playing_color is BLACK:
            return "Black"
        elif self._playing_color is WHITE:
            return "White"
        return None

    def add_piece(self, piece):
        self._board[piece.x][piece.y] = piece
        self._pieces.append(piece)

    def display(self):
        board = BOARD_FORMAT
        for x, y in CELLS:
            piece = self._board[x][y]
            r = " - " if (x + y) % 2 else "   "
            board = board.replace(
                "%s %s" % (x, y),
                repr(piece) if piece else r
            )
        print(board)

    def move(self, pos, npos):
        pos = Vector(*pos)
        npos = Vector(*npos)
        x, y = pos
        nx, ny = npos

        piece = self._board[x][y]
        if piece is None:
            raise InvalidMove("No piece on that position")
        elif piece.color is not self._playing_color:
            raise InvalidMove("You must move piece of your color")

        if nx < 0 or nx > 7 or ny < 0 or ny > 7:
            raise InvalidMove("Moving piece out of boundaries")

        move = piece.get_move(npos-pos)

        # Make sure you don't bumb into someone when moving:
        int_pos = pos.copy()
        for step in range(move.steps-1):
            int_pos += move
            ix, iy = int_pos
            if self._board[ix][iy]:
                raise InvalidMove("Bump into someone at (%s, %s)" % (ix, iy))
        # Check future
        npiece = self._board[nx][ny]
        if npiece:
            if npiece.color is self._playing_color:
                raise InvalidMove("Moving on a piece of your own")
            elif not move.can_kill:
                raise InvalidMove("Can't take a piece with this move")
        elif move.must_kill:
            raise InvalidMove("This move is valid only if it kills a piece")

        self._move(x, y, nx, ny, piece)

    def _move(self, x, y, nx, ny, piece):
        self._board[x][y] = None
        if self._board[nx][ny]:
            self._board[nx][ny].kill()
        piece.pos = (nx, ny)
        self._board[nx][ny] = piece
        self._playing_color = BLACK if self._playing_color is WHITE else WHITE


class Piece(object):

    def __init__(self, x, y, color):
        self._alife = True
        self._color = color
        self._direction = (
            Vector(1, 1) if self._color is BLACK else Vector(-1, 1)
        )
        self._pos = Vector(x, y)

        self._moves = None
        self._can_cross = False
        self.init_moves()

    def init_moves(self):
        raise NotImplementedError

    @property
    def alife(self):
        return self._alife

    @property
    def color(self):
        return self._color

    @property
    def dir(self):
        return self._direction

    @property
    def pos(self):
        return self._pos

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y

    @pos.setter
    def pos(self, npos):
        """Go not next position."""
        self._pos = Vector(npos[0], npos[1])

    def kill(self):
        self._alife = False

    def get_move(self, move_tuple):
        for move in self._moves:
            if move == move_tuple:
                return move
        raise InvalidMove(
            "%s can't do %s move."
            % (self.__class__.__name__, move_tuple)
        )

    def symbol(self):
        return "?"

    def __repr__(self):
        ind = "?"
        if self.color is WHITE:
            ind = "w"
        elif self.color is BLACK:
            ind = "b"
        return ind + self.symbol() + ind

    def __string__(self):
        return "{} ({}, {})".format(self.symbol(), *self.pos)


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


class King(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in itertools.product([-1, 0, 1], [-1, 0, 1]):
            if dpos == (0, 0):
                continue
            self._moves.append(Move(dpos))

    def symbol(self):
        return "K"


class Bishop(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in [(+1, +1), (+1, -1), (-1, +1), (-1, -1)]:
            for scal in range(1, 8):
                self._moves.append(Move(dpos, steps=scal))

    def symbol(self):
        return "B"


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


class Rook(Piece):

    def init_moves(self):
        self._moves = []
        for dpos in [(+1, 0), (0, -1), (0, +1), (-1, 0)]:
            for scal in range(1, 8):
                self._moves.append(Move(dpos, steps=scal))

    def symbol(self):
        return "R"


if __name__ == '__main__':
    print("++++ WELCOME TO CHESS ++++")
    print("\nHow to play:")
    print("\t- Specifiy your move such as 'a2 a4'")

    board = Board()
    board.display()

    def read_position(position):
        if len(position) != 2:
            raise InvalidMove("Cant' read position %s" % position)
        try:
            y = {
                'a': 0,
                'b': 1,
                'c': 2,
                'd': 3,
                'e': 4,
                'f': 5,
                'g': 6,
                'h': 7,
            }[position[0]]
        except KeyError:
            raise InvalidMove("Cant' read column %s" % position[0])
        try:
            x = 8 - int(position[1])
        except ValueError:
            raise InvalidMove("Cant' read column %s" % position[1])
        return x, y

    def read_input(message):
        r = message.split(" ")
        if len(r) != 2:
            raise InvalidMove("Cant' read move %s (needs 2 pos)" % message)
        pos = read_position(r[0])
        npos = read_position(r[1])
        return pos, npos

    cont = True
    while cont:
        try:
            print("\n%s is playing:" % board.player)
            message = input("\tMove:")
            pos, npos = read_input(message)
            board.move(pos, npos)
            board.display()
        except InvalidMove as e:
            print("/!\ InvalidMove :", e)
