from src.core.solver import SeatingSolver
from src.data.layouts import LIMOUSINE_LAYOUT
from src.entities import Passenger


def test_basic_assignment():
    passengers = [Passenger(id=1, name="Alice"), Passenger(id=2, name="Bob")]
    solver = SeatingSolver(LIMOUSINE_LAYOUT, passengers)
    results = solver.solve()

    # result is a dict, not a list!
    assert isinstance(results, dict)
    assert len(results) == 2
    # Check if seats are unique
    assert len(set(results.values())) == 2
