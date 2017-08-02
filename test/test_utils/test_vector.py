from utils.position import Position
from utils.vector import Vector


def test_Vector():
    origin = Position(0, 1)
    vector = Vector(-1, 2)
    points = [(-1, 3), (-2, 5)]
    for i, point in enumerate(vector.iter(origin, 2)):
        assert point == points[i]
