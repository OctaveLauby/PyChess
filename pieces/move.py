from utils.vector import Vector


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
