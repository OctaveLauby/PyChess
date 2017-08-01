from .vector import Vector
from .xyitem import XYItem


class Position(XYItem):
    def __sub__(self, other):
        if isinstance(other, Position):
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return super().__sub__(other)
