*This project has been created as part of the 42 curriculum by ckruk*

# Fly-in

## Description

**Fly-in** is a drone routing simulation built with a graphical visualization in Pygame. The goal is to move a fleet of drones from a start hub to an end hub through a network of connected zones (normal, restricted, priority, blocked) while respecting capacity constraints and minimizing simulation turns.

The program parses a map file, builds a graph, finds multiple paths using a modified Dijkstra algorithm (with priority zones favored), schedules drone movements turn by turn, and displays the whole simulation with animated drones.

## Instructions

### Compilation
```bash
make install
```

### Execution
```bash
make run
```

### Available Make Commands
```bash
make install      # Install dependencies (pygame, flake8, mypy)
make run          # Run the main program (main.py)
make debug        # Run in pdb debugger
make clean        # Remove __pycache__, .mypy_cache, .pytest_cache
make lint         # Run flake8 and mypy
make lint-strict  # Run flake8 and mypy --strict
```

## Algorithm Choices and Implementation Strategy

The project is fully object-oriented and split into modular components:

1. Parsing (parser.py)
A custom line-by-line parser validates the input file and builds Hub and Connection objects. It enforces syntax, metadata validity, unique names, bidirectional connections, and proper capacities. Errors raise a custom ParseError with line numbers.

2. Pathfinding (graph.py)
Paths are computed using Dijkstra's algorithm on a weighted adjacency list:
- normal = 1.0
- priority = 0.9 (so it is preferred over normal when lengths are equal)
- restricted = 2.0 (simulating the 2-turn transit cost)
- blocked = infinity (inaccessible)

To distribute drones across multiple paths, a find_paths function iteratively removes edges from the best path and recomputes Dijkstra, producing a set of alternative routes.

3. Simulation (simulation.py)
The simulation runs in discrete turns. Each drone holds a precomputed path and progresses turn-by-turn. The engine enforces:

- Zone capacity (max_drones) and connection capacity (max_link_capacity).
- Multi-turn transit for restricted zones (2 turns).
- Simultaneous movement with capacity freeing (drones leaving a hub free its slot in the same turn).
- Delivery detection and drone removal at the end hub.
- The start and end hubs have unlimited capacity by design.

4. Visualization (visualier.py)
The user interacts with a menu to pick a map. The simulation runs after pressing the right arrow (manual turn advancement). Drone movements are smoothly animated along graph edges. Hubs are colored based on their metadata. A final screen displays the number of turns when all drones are delivered.

## Visual Representation Features

The visualizer provides direct feedback on the simulation state:
- Menu screen: arrow keys navigate maps, ENTER starts the chosen map.
- Animated drones: smooth movement along connections, with drone IDs shown.
- Turn counter: displayed on top of the screen.
- Colored hubs: correspond to metadata (green, red, blue, orange, etc.) allowing users to visually distinguish zone types.
- Score screen: summarizes the total number of turns when all drones are delivered.
This helps peers and reviewers immediately understand how the algorithm is behaving on complex maps, including bottleneck accumulation, priority preference, and transit mechanics.


## Example Input and Expected Output

### Input (maps/easy/01_linear_path.txt)

nb_drones: 2

start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal

### Expected output

After running the program and selecting `Easy 1 - Linear path` from the menu, a Pygame window opens. 

The user can see:
1. A **start hub** (green) on the left and a **goal hub** (red) on the right.
2. Two intermediate hubs (`waypoint1` and `waypoint2`) colored blue, connected by white lines.
3. The text **"Turn 0"** at the top.

Pressing the **Right Arrow** advances the simulation turn by turn. The drones (displayed with their IDs) animate smoothly along the lines from hub to hub:
- **Turn 1:** D1 moves to waypoint1.
- **Turn 2:** D1 moves to waypoint2, D2 moves to waypoint1.
- **Turn 3:** D1 reaches the goal. D2 moves to waypoint2.
- **Turn 4:** D2 reaches the goal.

Once all drones are delivered, the screen displays a final message:
**"All drones delivered! Total number of turns: 4"**. 


## Resources

### References

- **Path finding**: https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1
- **Dijkstra**: https://www.geeksforgeeks.org/dsa/dijkstras-shortest-path-algorithm-greedy-algo-7/
- **Pygame tutorial**: https://medium.com/@moraneus/exploring-game-development-with-pygame-a-beginners-guide-58115caf9553
- **Drone picture**: https://pixabay.com/illustrations/flycam-mavic-mavic-mini-mini1-6820433/

### AI Usage

**AI was used for:**
- **Interpretation**: Help to interpretate instructions from the subject
- **Kick-off**: Help with understanding what is required in the project and what is it about to be able to start doing it
- **Explanation**: Guidance with new concepts without giving direct solutions
- **Testing**: Giving examples of cases to test the program
