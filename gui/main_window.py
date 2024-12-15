# gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QHBoxLayout
from gui.board import Board

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Evolution Project")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.board = Board()
        self.layout.addWidget(self.board)

        btn_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Evolution", self)
        self.start_button.clicked.connect(self.start_evolution)
        btn_layout.addWidget(self.start_button)

        self.layout.addLayout(btn_layout)

        self.stats_labels = []
        self.stats_layout = QVBoxLayout()
        self.layout.addLayout(self.stats_layout)

        self.generation_label = QLabel("Generation: 1", self)
        self.best_fitness_label = QLabel("Best Fitness: 0", self)
        self.layout.addWidget(self.generation_label)
        self.layout.addWidget(self.best_fitness_label)

        self.board.dots_updated.connect(self.update_stats)
        self.board.generation_updated.connect(self.update_generation_info)

    def start_evolution(self):
        self.board.add_dots(self.board.algorithm.population_size)
        self.board.add_food(20)
        self.board.start_food_timer(5000)
        self.board.start_food_depletion_timer(20000)
        self.update_stats()
        print("Evolution started.")

    def update_stats(self):
        for label in self.stats_labels:
            self.stats_layout.removeWidget(label)
            label.deleteLater()

        self.stats_labels = []
        for i, dot in enumerate(self.board.dots):
            status = "Dead" if dot.food_eaten <= 0 else f"Food: {dot.food_eaten:.2f}"
            label = QLabel(f"Dot #{i + 1} {status}", self)
            self.stats_labels.append(label)
            self.stats_layout.addWidget(label)

    def update_generation_info(self, generation, best_fitness):
        self.generation_label.setText(f"Generation: {generation}")
        self.best_fitness_label.setText(f"Best Fitness: {best_fitness:.2f}")
        print(f"Updated UI: Generation {generation}, Best Fitness {best_fitness}")
