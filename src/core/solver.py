from ortools.sat.python import cp_model
from src.entities import Seat, Passenger, Position, Orientation
from src.core.rules import get_manhattan_distance, is_neighbor, is_within_nuisance_range

class SeatingSolver:
    def __init__(self, seats: list[Seat], passengers: list[Passenger], name: str = "Puzzle"):
        self.seats = seats
        self.passengers = passengers
        self.name = name
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()
        
        # Variables: assignments[(p_id, s_id)] = 1 if passenger is in seat
        self.assignments = {}
        for p in self.passengers:
            for s in self.seats:
                self.assignments[(p.id, s.id)] = self.model.NewBoolVar(f'p{p.id}_s{s.id}')

    def display_grid(self, assignments, layout_name="LEVEL"):
        
        # Find dimension of the level
        max_x = max(s.x for s in self.seats)
        max_y = max(s.y for s in self.seats)
        
        # Creating the grid
        grid = [[" . " for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        
        # Place empty seats
        for s in self.seats:
            stype = s.position.value[0] if s.position else "?"
            grid[s.y][s.x] = f"({stype})"
            
        # Place characters
        for p, s in assignments:
            grid[s.y][s.x] = f"P{p.id:<2}"
            
        # Print final result
        print(f"\n{'='*10} {layout_name.upper()} PLAN {'='*10}")
        
        x_header = "      " + "".join(f" {x: <2}" for x in range(max_x + 1))
        print(x_header)
        print("    " + "──" * len(x_header))

        for y in range(max_y + 1):
            row_content = "".join(grid[y])
            print(f"Y={y} │ {row_content}")
            
        print(f"{'='*35}\n")
    
    def _add_inclusion_constraint(self, p, s, potential_neighbors):
        """Helper to force at least one neighbor if p is in s."""
        if potential_neighbors:
            self.model.Add(sum(potential_neighbors) >= 1).OnlyEnforceIf(self.assignments[(p.id, s.id)])
        else:
            self.model.Add(self.assignments[(p.id, s.id)] == 0)

    def _has_nuisance_conflict(self, p1, p2):
        """Centralizes all smell/noise/quiet logic."""
        bad_smell = (p1.hates_bad_smells and p2.smells_bad) or (p2.hates_bad_smells and p1.smells_bad)
        cologne = (p1.hates_cologne and p2.smells_cologne) or (p2.hates_cologne and p1.smells_cologne)
        talk = (p1.hates_talkative and p2.talkative) or (p2.hates_talkative and p1.talkative)
        music = (p1.hates_music and p2.plays_music) or (p2.hates_music and p1.plays_music)
        quiet = (p1.needs_quiet and (p2.talkative or p2.plays_music)) or \
                (p2.needs_quiet and (p1.talkative or p1.plays_music))
        return bad_smell or cologne or talk or music or quiet

    def _enforce_proximity_requirement(self, p1, filter_func):
        """Generic method to force p1 to be near at least one passenger matching filter_func."""
        for s1 in self.seats:
            potential_neighbors = []
            for p2 in self.passengers:
                if p1.id != p2.id and filter_func(p2):
                    # Getting the neighbors seats
                    potential_neighbors.extend([
                        self.assignments[(p2.id, s2.id)] 
                        for s2 in self.seats if is_neighbor(s1, s2)
                    ])
        
        # Apply the inclusion constraint
        self._add_inclusion_constraint(p1, s1, potential_neighbors)

    def _enforce_seat_requirement(self, p, seat_filter_func, attr_name):
        """Forces passenger p to be on a seat matching seat_filter_func."""
        valid_vars = [
            self.assignments[(p.id, s.id)] 
            for s in self.seats if seat_filter_func(s)
        ]
        
        if valid_vars:
            self.model.Add(sum(valid_vars) == 1)
        else:
            print(f"Warning: No seat found with {attr_name} for {p.name}")
    
    def solve(self):

        # Each passenger needs exactly 1 seat
        for p in self.passengers:
            self.model.AddExactlyOne(self.assignments[(p.id, s.id)] for s in self.seats)

        # Each seat max 1 passenger
        for s in self.seats:
            self.model.AddAtMostOne(self.assignments[(p.id, s.id)] for p in self.passengers)

        # SOCIAL CONSTRAINTS
        for p1 in self.passengers:

            if p1.talkative:
                self._enforce_proximity_requirement(p1, lambda p: p.talkative)

            # Rule: Nannies/Parents need to be near at least one child
            if p1.wants_to_be_near_child:
                self._enforce_proximity_requirement(p1, lambda p: p.is_child)

            # Exclusion loop P1 vs P2
            for p2 in self.passengers:
                if p1.id >= p2.id: continue 

                is_group = (p2.id in p1.must_be_near) or (p1.id in p2.must_be_near)
                is_rival = (p2.id in p1.hates) or (p1.id in p2.hates)

                for s1 in self.seats:
                    for s2 in self.seats:
                        if s1.id == s2.id: continue
                        dist = get_manhattan_distance(s1, s2)

                        # --- Rayon 1 (Neighbors) ---
                        if dist <= 1:
                            if p1.wants_to_be_alone or p2.wants_to_be_alone or \
                               (p1.dislikes_children and p2.is_child) or \
                               (p2.dislikes_children and p1.is_child) or is_rival:
                                self.model.Add(self.assignments[(p1.id, s1.id)] + self.assignments[(p2.id, s2.id)] <= 1)
                            
                        # --- Rayon 2 (Nuisances) ---
                        if dist <= 2 and not is_group:
                            if self._has_nuisance_conflict(p1, p2):
                                self.model.Add(self.assignments[(p1.id, s1.id)] + self.assignments[(p2.id, s2.id)] <= 1)
                        
                        # --- Grouping ---
                        if is_group and dist > 1:
                            self.model.Add(self.assignments[(p1.id, s1.id)] + self.assignments[(p2.id, s2.id)] <= 1)
            
                        
        for p in self.passengers:
            if p.prefers_window:
                self._enforce_seat_requirement(p, lambda s: s.position == Position.WINDOW, "Window")

            if p.prefers_forward:
                self._enforce_seat_requirement(p, lambda s: s.orientation == Orientation.FORWARD, "Forward")
        
        status = self.solver.Solve(self.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"\nSolution found! ({self.solver.StatusName(status)})")
            
            assigned_data = []
            # On crée un dictionnaire : {id_passager: id_siège}
            solution_map = {} 

            for p in self.passengers:
                for s in self.seats:
                    if self.solver.Value(self.assignments[(p.id, s.id)]):
                        # Garde tes logs pour la console
                        print(f"[ASSIGNED] {p.name:<12} -> Seat {s.id}")
                        
                        assigned_data.append((p, s))
                        solution_map[p.id] = s.id

            self.display_grid(assigned_data, layout_name=self.name)
            
            # On retourne le dictionnaire pour que les tests puissent l'utiliser
            return solution_map 
        else:
            print("No solution found.")
            return None