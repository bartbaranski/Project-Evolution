import random
import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_eaten = 0  # Liczba zjedzonych jedzeń

    def move_towards(self, target_x, target_y):
        # Przesuwanie w kierunku celu (jedzenia)
        direction_x = target_x - self.x
        direction_y = target_y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.x += direction_x
        self.y += direction_y

    def check_collision(self, food):
        # Sprawdzenie kolizji z jedzeniem
        distance = math.sqrt((self.x - food.x)**2 + (self.y - food.y)**2)
        return distance < 10  # Kolizja, jeśli odległość jest mniejsza niż 10

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board(QWidget):
    dots_updated = pyqtSignal()  # Sygnał do aktualizacji statystyk

    def __init__(self):
        super().__init__()
        self.initBoard()
        self.dots = []
        self.foods = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dots)

    def initBoard(self):
        self.setMinimumSize(600, 400)  # Zwiększ rozmiar planszy

    def add_dots(self, num_dots):
        self.dots = []
        for _ in range(num_dots):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            self.dots.append(Dot(x, y))
        self.update()
        self.timer.start(100)  # Aktualizacja co 100 ms

    def add_food(self, num_food):
        self.foods = []
        for _ in range(num_food):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            self.foods.append(Food(x, y))
        self.update()

    def update_dots(self):
        for dot in self.dots:
            if self.foods:
                # Znajdź najbliższe jedzenie
                closest_food = min(self.foods, key=lambda food: math.sqrt((dot.x - food.x)**2 + (dot.y - food.y)**2))
                dot.move_towards(closest_food.x, closest_food.y)
                # Sprawdź kolizję
                if dot.check_collision(closest_food):
                    dot.food_eaten += 1
                    self.foods.remove(closest_food)
        self.dots_updated.emit()  # Emituj sygnał do aktualizacji statystyk
        self.update()  # Wywołaj ponownie paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Rysowanie ramki
        rect = self.rect()
        pen = QPen(Qt.black, 4)
        painter.setPen(pen)
        painter.drawRect(rect)

        # Rysowanie kropek
        painter.setPen(Qt.NoPen)
        brush = QBrush(Qt.gray)
        painter.setBrush(brush)
        for dot in self.dots:
            painter.drawEllipse(int(dot.x), int(dot.y), 10, 10)  # Powiększone kropki, konwersja na int

        # Rysowanie jedzenia
        painter.setPen(Qt.NoPen)
        brush = QBrush(Qt.green)
        painter.setBrush(brush)
        for food in self.foods:
            points = [QPoint(int(food.x), int(food.y)), QPoint(int(food.x + 10), int(food.y)), QPoint(int(food.x + 5), int(food.y - 10))]
            painter.drawPolygon(*points)
