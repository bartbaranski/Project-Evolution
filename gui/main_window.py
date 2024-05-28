from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget
from algorithms.evolution import EvolutionAlgorithm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Evolution')
        self.algorithm = EvolutionAlgorithm()
        self.initUI()  # Wywołaj metodę initUI

    def initUI(self):
        self.start_button = QPushButton('Start Evolution')
        self.start_button.clicked.connect(self.start_evolution)
        layout = QVBoxLayout()
        layout.addWidget(self.start_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_evolution(self):
        self.algorithm.run()
