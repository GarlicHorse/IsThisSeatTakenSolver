import pytest
from src.entities import Passenger, Seat, Position, Orientation
from src.core.solver import SeatingSolver

def test_strict_window_requirement():
    seats = [
        Seat(id="Aisle_1", x=0, y=0, position=Position.AISLE, orientation=Orientation.FORWARD),
        Seat(id="Window_1", x=1, y=0, position=Position.WINDOW, orientation=Orientation.FORWARD)
    ]
    p1 = Passenger(id=1, name="Mia", prefers_window=True)
    
    solver = SeatingSolver(seats, [p1], name="Window Test")
    results = solver.solve()
    
    # results is {1: 'Window_1'}
    assert results is not None
    assert results[p1.id] == "Window_1"

def test_talkative_inclusion_logic():
    seats = [
        Seat(id="S1", x=0, y=0, position=Position.MIDDLE, orientation=Orientation.FORWARD),
        Seat(id="S2", x=1, y=0, position=Position.MIDDLE, orientation=Orientation.FORWARD),
        Seat(id="S3", x=5, y=5, position=Position.MIDDLE, orientation=Orientation.FORWARD)
    ]
    p1 = Passenger(id=1, name="Talker_A", talkative=True)
    p2 = Passenger(id=2, name="Talker_B", talkative=True)
    
    solver = SeatingSolver(seats, [p1, p2], name="Talkative Test")
    results = solver.solve()
    
    assert results is not None
    # Check that neither is on S3 (isolated)
    assert results[1] != "S3"
    assert results[2] != "S3"
    # They must be on S1 and S2
    assert set(results.values()) == {"S1", "S2"}

def test_must_be_near_grouping():
    seats = [
        Seat(id="S1", x=0, y=0, position=Position.MIDDLE, orientation=Orientation.FORWARD),
        Seat(id="S2", x=1, y=0, position=Position.MIDDLE, orientation=Orientation.FORWARD),
        Seat(id="S3", x=10, y=10, position=Position.MIDDLE, orientation=Orientation.FORWARD)
    ]
    p1 = Passenger(id=1, name="Friend_A", must_be_near=[2])
    p2 = Passenger(id=2, name="Friend_B", must_be_near=[1])
    
    solver = SeatingSolver(seats, [p1, p2], name="Group Test")
    results = solver.solve()
    
    assert results is not None
    # Verify both are on S1 and S2
    assigned_ids = set(results.values())
    assert "S1" in assigned_ids
    assert "S2" in assigned_ids