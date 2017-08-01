from utils.vector import Vector


class Move(Vector):
    def __init__(self, direction, steps=1, can_kill=True, must_kill=False):
        super().__init__(direction)
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

    def match(self, other):
        return self == other

    def __eq__(self, other):
        return Vector(self) * self.steps == other

    def __str__(self):
        return super().__str__() + "%s>" % self.steps
