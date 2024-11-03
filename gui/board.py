import random
import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal
from algorithms.evolution import EvolutionAlgorithm

class Dot:
    def __init__(self, x, y, speed=1):
        self.x = x
        self.y = y
        self.speed = speed
        self.food_eaten = 5  #starting amount of food
        self.target_x = None
        self.target_y = None

    def move_towards(self, target_x, target_y):
        direction_x = target_x - self.x
        direction_y = target_y - self.y
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed

    def check_collision(self, food):
        distance = math.sqrt((self.x - food.x)**2 + (self.y - food.y)**2)
        return distance < 10

    def choose_random_target(self, width, height):
        self.target_x = random.randint(0, width - 1)
        self.target_y = random.randint(0, height - 1)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board(QWidget):
    dots_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initBoard()
        self.dots = []
        self.foods = []
        self.algorithm = EvolutionAlgorithm()
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.update_dots)
        self.food_timer = QTimer(self)
        self.food_timer.timeout.connect(self.add_food_periodically)
        self.food_depletion_timer = QTimer(self)
        self.food_depletion_timer.timeout.connect(self.deplete_food)

    def initBoard(self):
        self.setMinimumSize(600, 400)

    def add_dots(self, num_dots):
        self.dots = []
        for _ in range(num_dots):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            speed = random.uniform(1, 3)
            dot = Dot(x, y, speed)
            dot.choose_random_target(self.width(), self.height())
            self.dots.append(dot)
        self.update()
        self.move_timer.start(100)  #dot position refrofreshed

    def add_food(self, num_food):
        for _ in range(num_food):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            self.foods.append(Food(x, y))
        self.update()

    def add_food_periodically(self):
        self.add_food(1)  #plus one food

    def start_food_timer(self, interval):
        self.food_timer.start(interval)

    def start_food_depletion_timer(self, interval):
        self.food_depletion_timer.start(interval)

    def deplete_food(self):
        for dot in self.dots:
            if dot.food_eaten > 0:
                dot.food_eaten -= 1
        self.dots_updated.emit()
        self.update()

    def update_dots(self):
        new_dots = []
        for dot in self.dots:
            if dot.food_eaten == 0:
                continue

            if self.foods:
                closest_food = min(self.foods, key=lambda food: math.sqrt((dot.x - food.x)**2 + (dot.y - food.y)**2))
                dot.move_towards(closest_food.x, closest_food.y)
                if dot.check_collision(closest_food):
                    dot.food_eaten += 1
                    self.foods.remove(closest_food)
                    if dot.food_eaten % 3 == 0:
                        new_dots.append(self.reproduce(dot))
                    dot.choose_random_target(self.width(), self.height())
            else:
                if dot.target_x is None or dot.target_y is None:
                    dot.choose_random_target(self.width(), self.height())
                dot.move_towards(dot.target_x, dot.target_y)
                if dot.check_collision(Food(dot.target_x, dot.target_y)):
                    dot.choose_random_target(self.width(), self.height())

        self.dots.extend(new_dots)
        while len(self.dots) > 10:
            self.dots.pop(0)
        self.dots_updated.emit()
        self.update()

    def reproduce(self, parent):
        child = Dot(parent.x, parent.y, parent.speed)
        self.algorithm.mutate(child)
        return child

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()
        pen = QPen(Qt.black, 4)
        painter.setPen(pen)
        painter.drawRect(rect)

        painter.setPen(Qt.NoPen)
        brush = QBrush(Qt.gray)
        painter.setBrush(brush)
        for dot in self.dots:
            if dot.food_eaten > 0:
                painter.drawEllipse(int(dot.x), int(dot.y), 10, 10)

        painter.setPen(Qt.NoPen)
        brush = QBrush(Qt.green)
        painter.setBrush(brush)
        for food in self.foods:
            points = [QPoint(int(food.x), int(food.y)), QPoint(int(food.x + 10), int(food.y)), QPoint(int(food.x + 5), int(food.y - 10))]
            painter.drawPolygon(*points)
