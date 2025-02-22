# ProjectEvolution

ProjectEvolution is a Python simulation that uses genetic algorithms to evolve simple neural networks. Agents, called "dots," navigate a 2D environment to collect food, with their performance measured by the amount of food consumed.

## Jupyter File
https://bartbaranski.github.io/Project-Evolution/reports/analysis_notebook.html

## Overview

- **Neural Networks:** Each dot is controlled by a simple neural network that determines its movement based on environmental inputs.
- **Evolutionary Algorithm:** An evolutionary process selects the best-performing dots via a roulette-wheel mechanism. New generations are produced using crossover and mutation techniques.
- **Real-Time Simulation:** The simulation features a PyQt5 graphical interface that visualizes dots moving in a 2D space, collecting food, and evolving over successive generations.
- **Data Logging:** Simulation data is logged to CSV files for analysis of each generation's performance.

## Features

- Evolving neural networks through genetic algorithms.
- Interactive 2D simulation with real-time visualization.
- Dynamic mutation rate adjustment based on performance improvement.
- CSV logging for detailed experiment data.

