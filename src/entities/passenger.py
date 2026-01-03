from dataclasses import dataclass, field


@dataclass
class Passenger:
    id: int
    name: str
    is_child: bool = False
    wants_to_be_alone: bool = False

    # Smell Related
    smells_bad: bool = False      
    smells_cologne: bool = False
    hates_bad_smells: bool = False
    hates_cologne: bool = False
    
    prefers_window: bool = False
    prefers_forward: bool = False
    dislikes_children: bool = False
    wants_to_be_near_child: bool = False

    # Social preference
    must_be_near: list[int] = field(default_factory=list)
    hates: list[int] = field(default_factory=list)

    # Noise related
    talkative: bool = False        
    hates_talkative: bool = False  
    plays_music: bool = False      
    hates_music: bool = False      
    needs_quiet: bool = False 