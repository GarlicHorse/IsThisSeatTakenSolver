from ortools.sat.python import cp_model
from src.entities import Seat, Passenger, Position, Orientation
from src.core.rules import get_manhattan_distance, is_neighbor, is_within_nuisance_range

class SeatingSolver:
    def __init__(self, seats: list[Seat], passengers: list[Passenger]):
        self.seats = seats
        self.passengers = passengers
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
        print(f"\n{'='*10} 🧩 {layout_name.upper()} PLAN {'='*10}")
        
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
    
    def solve(self):

        # Each passenger needs exactly 1 seat
        for p in self.passengers:
            self.model.AddExactlyOne(self.assignments[(p.id, s.id)] for s in self.seats)

        # Each seat max 1 passenger
        for s in self.seats:
            self.model.AddAtMostOne(self.assignments[(p.id, s.id)] for p in self.passengers)

        # SOCIAL CONSTRAINTS
        for p1 in self.passengers:
            # Condition Inclusion: Talkative
            if p1.talkative:
                for s1 in self.seats:
                    potential_talking_neighbors = []
                    for p2 in self.passengers:
                        if p2.talkative and p1.id != p2.id:
                            # Utilisation de is_neighbor
                            potential_talking_neighbors.extend([
                                self.assignments[(p2.id, s2.id)] 
                                for s2 in self.seats if is_neighbor(s1, s2)
                            ])
                    self._add_inclusion_constraint(p1, s1, potential_talking_neighbors)

            # Condition Inclusion: Nanny
            if p1.wants_to_be_near_child:
                for s1 in self.seats:
                    potential_kids_nearby = []
                    for p2 in self.passengers:
                        if p2.is_child and p2.id != p1.id:
                            potential_kids_nearby.extend([
                                self.assignments[(p2.id, s2.id)] 
                                for s2 in self.seats if is_neighbor(s1, s2)
                            ])
                    self._add_inclusion_constraint(p1, s1, potential_kids_nearby)

            # Boucle d'exclusion P1 vs P2
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
                # On force le passager sur l'un des sièges WINDOW
                window_vars = [self.assignments[(p.id, s.id)] for s in self.seats if s.position.value == "WINDOW"]
                if window_vars:
                    self.model.Add(sum(window_vars) == 1)
                else:
                    print(f"⚠️ Erreur Niveau : {p.name} veut une fenêtre mais il n'y en a pas !")

            if p.prefers_forward:
                # On force le passager sur l'un des sièges FORWARD
                forward_vars = [self.assignments[(p.id, s.id)] for s in self.seats if s.orientation == Orientation.FORWARD]
                if forward_vars:
                    self.model.Add(sum(forward_vars) == 1)
        


        status = self.solver.Solve(self.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(f"\nSolution found! (Status: {self.solver.StatusName(status)})")
            
            # On stocke les résultats sous forme d'objets pour la visualisation
            assigned_data = []
            final_output = []

            for p in self.passengers:
                for s in self.seats:
                    if self.solver.Value(self.assignments[(p.id, s.id)]):
                        log_msg = f"[ASSIGNED] {p.name:<12} -> Seat {s.id:<5} (x={s.x}, y={s.y})"
                        
                        # Log des raisons spécifiques (debug)
                        if p.smells_bad: log_msg += " [!] Smelly"
                        if p.smells_cologne: log_msg += " [!] Cologne"
                        if p.is_child: log_msg += " [c] Child"
                        
                        print(log_msg)
                        assigned_data.append((p, s))
                        final_output.append(f"Passenger {p.name} -> Seat {s.id}")

            self.display_grid(assigned_data)
            return final_output
        else:
            print("No solution found.")
            return "No solution found."