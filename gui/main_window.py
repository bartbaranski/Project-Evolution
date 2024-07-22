from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel
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

        self.start_button = QPushButton("Start Evolution", self)
        self.start_button.clicked.connect(self.start_evolution)
        self.layout.addWidget(self.start_button)

        self.stats_labels = []
        self.stats_layout = QVBoxLayout()
        self.layout.addLayout(self.stats_layout)

    def start_evolution(self):
        self.board.add_dots(10)  # Inicjalizuje 10 kropek
        self.board.add_food(5)   # Inicjalizuje jedzenie, możesz dostosować liczbę jedzenia
        self.board.start_food_timer(5000)  # Dodaje jedzenie co 5 sekund
        self.board.start_food_depletion_timer(20000)  # Zmniejsza jedzenie co 20 sekund
        self.update_stats()
        self.board.dots_updated.connect(self.update_stats)

    def update_stats(self):
        # Usuwamy istniejące etykiety
        for label in self.stats_labels:
            self.stats_layout.removeWidget(label)
            label.deleteLater()

        self.stats_labels = []

        # Dodajemy nowe etykiety
        for i, dot in enumerate(self.board.dots):
            status = "Dead" if dot.food_eaten == 0 else f"Food: {dot.food_eaten}"
            label = QLabel(f"Dot #{i + 1} {status}", self)
            self.stats_labels.append(label)
            self.stats_layout.addWidget(label)
