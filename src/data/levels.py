from src.entities import Passenger


def get_london_level_1_1():
    return [
        Passenger(id=1, name="Mia", smells_bad=True, prefers_window=True),
        Passenger(id=2, name="Freia", smells_cologne=True),
        Passenger(id=3, name="Nisa", must_be_near=[2]),
        Passenger(
            id=4,
            name="Anastasiya",
            is_child=True,
            prefers_forward=True,
            wants_to_be_near_child=True,
        ),
        Passenger(id=5, name="Li", must_be_near=[1], is_child=True),
        Passenger(
            id=6,
            name="Harper",
            wants_to_be_alone=True,
            hates_bad_smells=True,
            hates_cologne=True,
        ),
        Passenger(id=7, name="Oliver", wants_to_be_alone=True, prefers_window=True),
        Passenger(id=8, name="Atlas", hates_bad_smells=True),
    ]


def get_london_level_1_2():
    return [
        Passenger(id=1, name="Nat", prefers_window=True),
        Passenger(id=2, name="Derry", hates_music=True, talkative=True),
        Passenger(id=3, name="Angela", hates_talkative=True),
        Passenger(id=4, name="Rei", needs_quiet=True),
        Passenger(id=5, name="Maku", talkative=True),
        Passenger(id=6, name="Ryo", plays_music=True),
        Passenger(id=7, name="Samuel", hates_music=True),
        Passenger(id=8, name="Tony", prefers_forward=True, plays_music=True),
        Passenger(id=9, name="Barrie", hates=[8], plays_music=True),
    ]


def get_london_level_1_3():
    return [
        Passenger(id=1, name="Nico", hates_bad_smells=True, talkative=True),
        Passenger(id=2, name="Kai", hates_bad_smells=True),
        Passenger(id=3, name="Dorian", hates_talkative=True),
        Passenger(id=4, name="Wyatt", hates_bad_smells=True, smells_bad=True),
        Passenger(
            id=5, name="David", plays_music=True, smells_bad=True, hates_talkative=True
        ),
        Passenger(id=6, name="Emma", needs_quiet=True),
        Passenger(id=7, name="Teo", hates=[9]),
        Passenger(id=8, name="Victor", talkative=True),
        Passenger(id=9, name="Noah", must_be_near=[4]),
    ]
