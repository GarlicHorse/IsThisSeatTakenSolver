from dataclasses import dataclass
from enum import Enum


class Position(Enum):
    WINDOW = "WINDOW"
    AISLE = "AISLE"
    MIDDLE = "MIDDLE"

class Orientation(Enum):
    FORWARD = "FORWARD"
    BACKWARD = "BACKWARD"

@dataclass(frozen=True)
class Seat:
    id: str
    x: int  # x coordinate in layout 
    y: int  # y coordinate in layout
    position: Position
    orientation: Orientation