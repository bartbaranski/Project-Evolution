<h1>Evolution Simulation Project</h1>
This project is a Python-based evolutionary simulation that visualizes autonomous entities (dots) moving on a board, seeking food and reproducing based on resource availability. The project demonstrates a simple evolutionary algorithm with principles of natural selection, mutation, and reproduction.

<h2>Features</h2>
<ul>
  <li>Autonomous Dots: Entities (dots) navigate the board, searching for food. Their movement and reproduction depend on food consumption.</li>
  <li>Food Mechanics: Food items (green triangles) spawn periodically on the board. Dots that consume food can reproduce; those that deplete their food levels die.</li>
  <li>Evolutionary Algorithm: Each entity can mutate slightly when reproducing, simulating evolution and adaptation over time.</li>
  <li>Live Statistics: The UI displays real-time statistics for each dot, including its current food level and status (alive or dead).</li>
</ul>
<h2>Technologies</h2>
<ul>
<li>Python: Core logic, algorithms, and object-oriented structure.</li>
<li>PyQt5: GUI components, including the simulation board and real-time updates.</li>
<li>Randomized Behavior: Randomized spawning locations and food consumption mechanics.</li>
<li>Evolutionary Dynamics: Mutation and selection within a simple evolutionary algorithm framework.</li>
</ul>
<h2>Usage</h2>
<ul>
<li>Start Simulation: Click the "Start Evolution" button in the GUI.</li>
<li>Observe: Watch dots navigate towards food, reproduce, and adapt over time.</li>
<li>Statistics: Check each dot’s food level and status on the side panel.</li>
</ul>
<h2>Future Improvements</h2>
<ul>
<li>Enhanced mutation mechanics with additional traits (e.g., speed, size).</li>
<li>Smarter pathfinding or neural network integration.</li>
<li>Expanded GUI features, including customizable settings for population and mutation rate.</li>
</ul>
