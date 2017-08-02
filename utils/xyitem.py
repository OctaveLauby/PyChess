import itertools


class XYItem(object):

    def __init__(self, x_or_xy, y=None):
        self.x = None
        self.y = None
        self.set(x_or_xy, y)

    @property
    def t(self):
        """Return x, y tuple."""
        return (self.x, self.y)

    def copy(self):
        """Return a copy."""
        return self.__class__(self.x, self.y)

    def set(self, x_or_xy, y=None):
        """Set x, y."""
        if isinstance(x_or_xy, XYItem):
            self.x = x_or_xy.x
            self.y = x_or_xy.y
        elif isinstance(x_or_xy, (list, tuple)):
            assert len(x_or_xy) == 2
            self.x = x_or_xy[0]
            self.y = x_or_xy[1]
        else:
            assert y is not None
            self.x = x_or_xy
            self.y = y

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if isinstance(other, XYItem):
            return self.t == other.t
        elif isinstance(other, (list, tuple)):
            return self.t == tuple(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.__class__(other*self.x, other*self.y)
        return self.__class__(self.x*other.x, self.y*other.y)

    def __rmul__(self, other):
        return self * other

    def __repr__(self):
        return self.__class__.__name__ + str(self)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __str__(self):
        return str(self.t)

    @staticmethod
    def iter(*shape):
        """Iter on multi dim ranges."""
        return itertools.product(*[range(i) for i in shape])


if __name__ == "__main__":
    v1 = XYItem(1, 1)
    v2 = XYItem(0, 1)
    assert str(v1) == "(1, 1)"
    assert repr(v1) == "XYItem(1, 1)"
    assert v1 + v2 == [1, 2]
    assert v1 * 5 == [5, 5]
    assert (v1 * v2) == (0, 1)
    assert v1 * v2 == [0, 1]
