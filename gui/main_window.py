from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QScrollArea, QFrame
from algorithms.evolution import EvolutionAlgorithm
from gui.board import Board

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Evolution')
        self.algorithm = EvolutionAlgorithm()
        self.num_dots = 50  # Liczba kropek do narysowania
        self.num_food = 20  # Liczba jedzenia do narysowania
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)  # Zwiększ rozmiar okna

        self.start_button = QPushButton('Start Evolution')
        self.start_button.clicked.connect(self.start_evolution)
        
        self.board = Board()  # Utwórz widżet planszy
        self.board.dots_updated.connect(self.update_stats)  # Połącz sygnał dots_updated z metodą update_stats

        self.stats_area = QScrollArea()
        self.stats_area.setWidgetResizable(True)
        self.stats_content = QWidget()
        self.stats_layout = QVBoxLayout(self.stats_content)
        self.stats_area.setWidget(self.stats_content)

        self.stats_labels = []
        for i in range(self.num_dots):
            label = QLabel(f"Dot #{i + 1} Food: 0")
            self.stats_labels.append(label)
            self.stats_layout.addWidget(label)

        layout = QHBoxLayout()
        layout.addWidget(self.board)  # Dodaj planszę do układu
        layout.addWidget(self.stats_area)

        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.start_button)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_evolution(self):
        self.board.add_dots(self.num_dots)
        self.board.add_food(self.num_food)
        self.update_stats()
        self.algorithm.run()

    def update_stats(self):
        for i, dot in enumerate(self.board.dots):
            self.stats_labels[i].setText(f"Dot #{i + 1} Food: {dot.food_eaten}")
