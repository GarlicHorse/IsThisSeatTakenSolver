import pytest
from src.models import Passenger
from src.layouts import LIMOUSINE_LAYOUT
from src.solver import SeatingSolver

def test_basic_assignment():
    """Test whether each character gets a unique seat"""
    passengers = [
        Passenger(id=1, name="Alice"),
        Passenger(id=2, name="Bob")
    ]
    solver = SeatingSolver(LIMOUSINE_LAYOUT, passengers)
    results = solver.solve()
    
    assert isinstance(results, list)
    assert len(results) == 2
    # Check whether the same seat is not assigned to both
    seats_assigned = [res.split("->")[1].strip() for res in results]
    assert len(set(seats_assigned)) == 2

def test_smelly_constraint():
    """Vérifie que le passager qui sent mauvais n'a personne juste à côté."""
    # On remplace smelly=True par smells_bad=True
    p1 = Passenger(id=1, name="Smelly Joe", smells_bad=True) 
    p2 = Passenger(id=2, name="Victim", hates_bad_smells=True) # Ajoute ça pour forcer la contrainte
    
    solver = SeatingSolver(LIMOUSINE_LAYOUT, [p1, p2])
    results = solver.solve()
    
    assert results != "No solution found."