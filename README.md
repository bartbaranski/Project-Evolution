<h1>Evolution Simulation Project</h1>
This project is a Python-based evolutionary simulation that visualizes autonomous entities (dots) moving on a board, seeking food and reproducing based on resource availability. The project demonstrates a simple evolutionary algorithm with principles of natural selection, mutation, and reproduction.

Features
Autonomous Dots: Entities (dots) navigate the board, searching for food. Their movement and reproduction depend on food consumption.
Food Mechanics: Food items (green triangles) spawn periodically on the board. Dots that consume food can reproduce; those that deplete their food levels die.
Evolutionary Algorithm: Each entity can mutate slightly when reproducing, simulating evolution and adaptation over time.
Live Statistics: The UI displays real-time statistics for each dot, including its current food level and status (alive or dead).
Technologies
Python: Core logic, algorithms, and object-oriented structure.
PyQt5: GUI components, including the simulation board and real-time updates.
Randomized Behavior: Randomized spawning locations and food consumption mechanics.
Evolutionary Dynamics: Mutation and selection within a simple evolutionary algorithm framework.
