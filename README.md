# 🧩 Is This Seat Taken? Solver

![Project Banner](assets/banner.avif)

A high-performance logic puzzle engine designed to solve levels from the game **"Is This Seat Taken?"**. This project transforms complex human social behaviors and seating preferences into a **Constraint Satisfaction Problem (CSP)** using mathematical optimization.

## 🚀 Overview

In "Is This Seat Taken?", the challenge is to seat a diverse group of passengers in various vehicles (Taxis, Limos, Buses, etc.). Every passenger comes with specific needs, quirks, and social boundaries. 

This solver uses **Google OR-Tools (CP-SAT)** to navigate millions of possible seating combinations in milliseconds to find the one unique configuration that satisfies every single non-negotiable requirement.

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

## 📖 How to Contribute
1.  Add new **Passenger Profiles** in `passengers.py`.
2.  Map new **Vehicle Layouts** in `layouts.py`.
3.  Improve the **Grid Visualization** in the terminal.