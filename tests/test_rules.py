from src.entities.seat import Seat, Position, Orientation
from src.core.rules import get_manhattan_distance, is_neighbor

def test_manhattan_distance():
    s1 = Seat(id="1", x=0, y=0, position=Position.WINDOW, orientation=Orientation.FORWARD)
    s2 = Seat(id="2", x=1, y=1, position=Position.WINDOW, orientation=Orientation.FORWARD)
    # distance = |0-1| + |0-1| = 2
    assert get_manhattan_distance(s1, s2) == 2

def test_is_neighbor():
    s1 = Seat(id="1", x=0, y=0, position=Position.WINDOW, orientation=Orientation.FORWARD)
    s2 = Seat(id="2", x=0, y=1, position=Position.WINDOW, orientation=Orientation.FORWARD)
    assert is_neighbor(s1, s2) is True