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


if __name__ == "__main__":
    v1 = Vector(1, 1)
    v2 = Vector(0, 1)
    assert v1 + v2 == [1, 2]
    assert v1 * 5 == [5, 5]
    assert v1 * v2 == [0, 1]
