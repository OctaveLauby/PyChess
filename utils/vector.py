from .xyitem import XYItem


class Vector(XYItem):

    def iter(self, position, steps):
        int_pos = position
        for step in range(steps):
            int_pos = int_pos + self
            yield int_pos
