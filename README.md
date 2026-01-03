# 🧩 Is This Seat Taken? Solver

[![Python Tests](https://github.com/GarlicHorse/IsThisSeatTakenSolver/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/GarlicHorse/IsThisSeatTakenSolver/actions/workflows/test.yml)

![Project Banner](assets/banner.avif)

A high-performance logic puzzle engine designed to solve levels from the game **"Is This Seat Taken?"**. This project transforms complex human social behaviors and seating preferences into a **Constraint Satisfaction Problem (CSP)** using mathematical optimization.

## 🚀 Overview

In "Is This Seat Taken?", the challenge is to seat a diverse group of passengers in various vehicles (Taxis, Limos, Buses, etc.). Every passenger comes with specific needs, quirks, and social boundaries. 

This solver uses **Google OR-Tools (CP-SAT)** to navigate millions of possible seating combinations in milliseconds to find the one unique configuration that satisfies every single non-negotiable requirement.

## 🧠 Understanding Constraint Satisfaction Problems (CSP)

At its core, this engine treats seating challenges as a **Constraint Satisfaction Problem (CSP)**. Instead of using imperative logic (telling the computer *how* to find a seat step-by-step), we use **declarative logic** (defining *what* the valid final state looks like).

A CSP is defined by three mathematical components:

1. **Variables ($V$):** The entities that need to be assigned. In this engine, each **Passenger** is a variable that needs to be "solved" by finding the correct seat coordinate.
2. **Domains ($D$):** The set of all possible values for each variable. For a passenger, the domain is the **list of available seats** $(x, y)$ within the grid.
3. **Constraints ($C$):** The rules that limit which values variables can take.
    * **Unary Constraints:** Rules affecting a single variable (e.g., *"Passenger A must be in a Window seat"*).
    * **Binary Constraints:** Rules affecting pairs (e.g., *"Passenger A cannot be within a Manhattan distance of 2 from Passenger B"*).
    * **Global Constraints:** System-wide rules (e.g., *"All assigned seats must be unique"*).



---

## ⚙️ How the Engine Works

The **Google OR-Tools CP-SAT** solver avoids "Brute Force" by combining two powerful techniques:

### Constraint Propagation
As soon as a choice is made, the solver "prunes" the domains of all other variables. If Passenger A is assigned to Seat 1, Seat 1 is immediately removed from the domains of all other passengers. This creates a "ripple effect" that eliminates millions of impossible configurations instantly.

### Backtracking Search
The solver builds a **Decision Tree**. It makes an assignment, propagates the consequences, and moves to the next variable. If it hits a **contradiction** (where a variable has no possible values left in its domain), it **backtracks** to the last valid state and tries a different branch.



### Spatial Abstraction
This mathematical approach makes the engine **environment-agnostic**. It doesn't perceive a "Bus" or a "Cinema"; it only sees a coordinate system where physical walls, aisles, or social bubbles are simply mathematical boundaries translated into the Manhattan Distance formula:
$$d(A, B) = |x_1 - x_2| + |y_1 - y_2|$$


## 🛋️ Supported Layouts

The game features various environments. While the engine is universal, we are currently implementing the following layouts:

* 🚕 **Taxi**: Small, cramped spaces with high proximity.
* 🚗 **Limousine**: Reverse U-shaped or face-to-face seating arrangements.

> **🤝 Contribution Goal**: We are actively looking to complete the library of layouts! If you have mapped a vehicle or a specific level grid, feel free to submit a **Pull Request**.

## 🧠 Core Logic & Constraints

The engine handles multiple layers of logic:

### 1. Physical Requirements (Strict)
* **Environmental Needs**: Requirements for **Window Seats** or **Forward-Facing** orientations are treated as hard constraints.
* **Uniqueness**: Each passenger gets exactly one seat; each seat takes max one passenger.

### 2. Proximity & Social Needs
* **Groups & Pairs**: Friends (`must_be_near`) are forced into adjacent seats (Manhattan Distance = 1).
* **The "Nanny" Rule**: Caregivers must be adjacent to at least one `is_child` passenger.
* **Social Butterflies**: Talkative passengers are only satisfied if they have another talkative neighbor.
* **Solitary Travelers**: Some passengers trigger a conflict if any neighbor is detected within their personal bubble.

### 3. Nuisance & Exclusion Zones
The solver calculates **Manhattan Distance** ($|x_1 - x_2| + |y_1 - y_2|$) to enforce exclusion radii:
* **Scent & Noise**: Exclusion zones for bad smells, loud music, or strong cologne.
* **Quiet Zones**: Specific placement for passengers who `need_quiet`.
* **Personal Rivalries**: Prevents "Hated" individuals from being seated within a specific radius.

## 🛠️ Technical Stack
* **Python 3.10+**
* **Google OR-Tools**: CP-SAT Solver.
* **Python Dataclasses**: For clean, extensible definitions.

## 🚀 How to Use

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/GarlicHorse/IsThisSeatTakenSolver.git
cd IsThisSeatTakenSolver

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
## 🛠️ How to Contribute

This project is built to be modular. To add new game mechanics or characters, follow this **3-step workflow**:

### 1. Update the Dataclasses
If your new passenger or seat requires a trait that doesn't exist yet, add it to the corresponding dataclass in `src/entities.py`:
* **Passenger**: Add attributes such as `is_allergic`, `has_dog`, `needs_plug`, etc.
* **Seat**: Add attributes like `has_table`, `is_broken`, or `is_luxury`.

### 2. Implement the Rules in the Solver
Once the attribute exists, you must tell the engine how to handle it in `src/core/solver.py`:
* **For Exclusions (Nuisances):** Update the `_has_nuisance_conflict` method.
* **For Inclusions (Proximity):** Use the `_enforce_proximity_requirement` method with a custom lambda.
* **For Seat Requirements:** Use the `_enforce_seat_requirement` method.



### 3. Create Content & Test
* **Data:** Add your new passengers to `src/data/passengers.py` or layouts to `src/data/layouts.py`.
* **Verification:** Create a dedicated test case in `tests/test_logic.py` to ensure the rule is strictly enforced.
* **Execution:** Run `pytest` to verify that your new logic doesn't break existing levels.

## 🧪 Quality Standards
* **Type Safety:** Always use the defined `Enums` (`Position`, `Orientation`) instead of raw strings.
* **Non-Breaking Changes:** All previous levels must still be solvable after your changes.
* **Clarity:** Keep the `display_grid` output readable even when adding new seat types.