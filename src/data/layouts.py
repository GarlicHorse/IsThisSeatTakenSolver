from src.entities import Orientation, Position, Seat

TAXI_LAYOUT = [
    # BACKSEATS OF THE TAXI
    Seat(
        id="Rank-1-1",
        x=0,
        y=1,
        position=Position.WINDOW,
        orientation=Orientation.FORWARD,
    ),
    Seat(
        id="Rank-2-1",
        x=0,
        y=2,
        position=Position.MIDDLE,
        orientation=Orientation.FORWARD,
    ),
    Seat(
        id="Rank-3-1",
        x=0,
        y=3,
        position=Position.WINDOW,
        orientation=Orientation.FORWARD,
    ),
]

LIMOUSINE_LAYOUT = [
    # SEATS AGAINST THE BACK WINDOW (Rank 1)
    Seat(
        id="Rank-1-1",
        x=0,
        y=0,
        position=Position.WINDOW,
        orientation=Orientation.FORWARD,
    ),
    Seat(
        id="Rank-1-2",
        x=2,
        y=0,
        position=Position.MIDDLE,
        orientation=Orientation.BACKWARD,
    ),
    Seat(
        id="Rank-1-3",
        x=3,
        y=0,
        position=Position.MIDDLE,
        orientation=Orientation.BACKWARD,
    ),
    Seat(
        id="Rank-1-4",
        x=4,
        y=0,
        position=Position.MIDDLE,
        orientation=Orientation.BACKWARD,
    ),
    Seat(
        id="Rank-1-5",
        x=6,
        y=0,
        position=Position.WINDOW,
        orientation=Orientation.BACKWARD,
    ),
    # SEATS IN THE MIDDLE (RANK 2)
    Seat(
        id="Rank-2-1",
        x=0,
        y=1,
        position=Position.MIDDLE,
        orientation=Orientation.FORWARD,
    ),
    Seat(
        id="Rank-3-1",
        x=0,
        y=2,
        position=Position.WINDOW,
        orientation=Orientation.FORWARD,
    ),
    # SEATS AGAINST THE FRONT WINDOW (RANK 3)
    Seat(
        id="Rank-2-2",
        x=6,
        y=1,
        position=Position.MIDDLE,
        orientation=Orientation.BACKWARD,
    ),
    Seat(
        id="Rank-3-2",
        x=6,
        y=2,
        position=Position.WINDOW,
        orientation=Orientation.BACKWARD,
    ),
]
