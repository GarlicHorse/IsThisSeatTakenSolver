from src.entities import Seat

def get_manhattan_distance(s1: Seat, s2: Seat) -> int:
    """Calculates the Manhattan distance between two seats."""
    return abs(s1.x - s2.x) + abs(s1.y - s2.y)

def is_neighbor(s1: Seat, s2: Seat) -> bool:
    """Check if two seats are immediate neighbors (Radius 1)."""
    return get_manhattan_distance(s1, s2) == 1

def is_within_nuisance_range(s1: Seat, s2: Seat) -> bool:
    """Check if two seats are within nuisance range (Radius 2)."""
    return get_manhattan_distance(s1, s2) <= 2