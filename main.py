from src.entities import Passenger, Seat, Position, Orientation
from src.core.solver import SeatingSolver
from src.data.layouts import LIMOUSINE_LAYOUT
from src.data.levels import *

def play_level(city, level_num, layout, passengers):
    print(f"\n--- 🌍 {city.upper()} : LEVEL {level_num} ---")
    print(f"Goal: Place {len(passengers)} passengers with conflicting needs.")
    
    solver = SeatingSolver(layout, passengers)
    results = solver.solve()
    
    if results == "No solution found.":
        print("Impossible to satisfy everyone!")
    else:
        print("Succesful !")


if __name__ == "__main__":
    # Launch London Level 1
    play_level("London", 1,LIMOUSINE_LAYOUT, get_london_level_1_1())