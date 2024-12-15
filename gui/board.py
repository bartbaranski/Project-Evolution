# gui/board.py
import csv
import random
import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal
from algorithms.evolution import EvolutionAlgorithm
from algorithms.neural_network import SimpleNeuralNetwork

class Dot:
    _id_counter = 0
    def __init__(self, x, y, speed=1, network=None, birth_generation=0):
        self.x = x
        self.y = y
        self.speed = speed
        self.food_eaten = 5
        self.max_food_eaten = 5.0
        self.network = network if network is not None else SimpleNeuralNetwork()
        self.last_x = x
        self.last_y = y
        self.birth_generation = birth_generation
        self.id = Dot._id_counter
        Dot._id_counter += 1

    def set_food_eaten(self, new_value):
        self.food_eaten = new_value
        if self.food_eaten > self.max_food_eaten:
            self.max_food_eaten = self.food_eaten

    def decide_move(self, nearest_food, board_width, board_height, foods):
        nx = self.x / board_width
        ny = self.y / board_height

        if nearest_food is not None:
            nfx = nearest_food.x / board_width
            nfy = nearest_food.y / board_height
        else:
            nfx = 0.5
            nfy = 0.5

        f_level = min(self.food_eaten / 10.0, 1.0)

        radius = 50.0
        nearby_food_count = sum(1 for f in foods if (f.x - self.x)**2 + (f.y - self.y)**2 < radius**2)
        food_density = min(nearby_food_count / 10.0, 1.0)

        dist_left = self.x
        dist_right = board_width - self.x
        dist_top = self.y
        dist_bottom = board_height - self.y
        min_dist_edge = min(dist_left, dist_right, dist_top, dist_bottom)
        half_min_dim = min(board_width, board_height) / 2.0
        boundary_dist = min_dist_edge / half_min_dim
        if boundary_dist > 1.0:
            boundary_dist = 1.0

        inputs = [nx, ny, nfx, nfy, f_level, food_density, boundary_dist]
        dx, dy = self.network.forward(inputs)
        return dx * self.speed, dy * self.speed

    def check_collision(self, food):
        distance = math.sqrt((self.x - food.x)**2 + (self.y - food.y)**2)
        return distance < 10

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board(QWidget):
    dots_updated = pyqtSignal()
    generation_updated = pyqtSignal(int, float)

    def __init__(self):
        super().__init__()
        self.initBoard()
        self.dots = []
        self.foods = []
        self.algorithm = EvolutionAlgorithm()
        
        self.steps_per_generation = 1000  # Increased steps
        self.current_step = 0

        # Logging data
        self.experiment_data = []
        self.output_csv = "simulation_report.csv"

        # Keep track of all dots ever created
        self.all_dots_record = {}

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
        Dot._id_counter = 0
        for _ in range(num_dots):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            speed = random.uniform(1, 3)
            dot = Dot(x, y, speed, birth_generation=self.algorithm.generation)
            self.all_dots_record[dot.id] = {"dot": dot, "food_when_died": None}
            self.dots.append(dot)
        print(f"Added {len(self.dots)} initial dots.")

        # Add a large cluster of food in the center to encourage movement inward
        center_x = self.width() // 2
        center_y = self.height() // 2
        for _ in range(50):
            fx = random.randint(center_x - 50, center_x + 50)
            fy = random.randint(center_y - 50, center_y + 50)
            self.foods.append(Food(fx, fy))
        print(f"Added 50 food items in the center.")

        # Add a slight bias to output layer biases to encourage movement
        for d in self.dots:
            d.network.b2 = [b + 0.2 for b in d.network.b2]
        print("Added bias to neural networks to encourage movement.")

        self.update()
        self.move_timer.start(100)
        print("Started move timer.")

    def add_food(self, num_food):
        for _ in range(num_food):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            self.foods.append(Food(x, y))
        print(f"Added {num_food} new food items.")
        self.update()

    def add_food_periodically(self):
        num_food = random.randint(2, 5)
        self.add_food(num_food)

    def start_food_timer(self, interval):
        self.food_timer.start(interval)
        print(f"Started food timer with interval {interval}ms.")

    def start_food_depletion_timer(self, interval):
        self.food_depletion_timer.start(interval)
        print(f"Started food depletion timer with interval {interval}ms.")

    def deplete_food(self):
        for dot in self.dots:
            if dot.food_eaten > 0:
                dot.set_food_eaten(dot.food_eaten - 1)
        print("Depleted food for all dots by 1.")
        self.dots_updated.emit()
        self.update()

    def update_dots(self):
        self.current_step += 1
        print(f"Step {self.current_step}/{self.steps_per_generation}")

        old_dot_ids = set(d.id for d in self.dots)

        for dot in self.dots:
            if dot.food_eaten <= 0:
                continue

            closest_food = None
            old_dist = None
            if self.foods:
                closest_food = min(self.foods, key=lambda f: (f.x - dot.x)**2 + (f.y - dot.y)**2)
                old_dist = math.sqrt((dot.x - closest_food.x)**2 + (dot.y - closest_food.y)**2)

            old_x, old_y = dot.x, dot.y
            dx, dy = dot.decide_move(closest_food, self.width(), self.height(), self.foods)

            new_x = dot.x + dx
            new_y = dot.y + dy
            new_x = max(0, min(self.width() - 10, new_x))
            new_y = max(0, min(self.height() - 10, new_y))
            dot.x, dot.y = new_x, new_y

            if closest_food and dot.check_collision(closest_food):
                dot.set_food_eaten(dot.food_eaten + 3)
                self.foods.remove(closest_food)
                print(f"Dot {dot.id} collided with food. Food eaten: {dot.food_eaten}")

            if closest_food:
                new_dist = math.sqrt((dot.x - closest_food.x)**2 + (dot.y - closest_food.y)**2)
                if old_dist is not None and new_dist < old_dist:
                    dot.set_food_eaten(dot.food_eaten + 0.1
                    )
                if new_dist > 100:
                    dot.set_food_eaten(dot.food_eaten - 0.01)

            dist_moved = math.sqrt((dot.x - old_x)**2 + (dot.y - old_y)**2)
            # Reward for significant movement
            if dist_moved > 5:
                dot.set_food_eaten(dot.food_eaten + 0.1
                )
                print(f"Dot {dot.id} moved significantly. Food eaten: {dot.food_eaten}")

            # Strong penalty for staying near edges
            dist_left = dot.x
            dist_right = self.width() - dot.x
            dist_top = dot.y
            dist_bottom = self.height() - dot.y
            min_dist_edge = min(dist_left, dist_right, dist_top, dist_bottom)
            if min_dist_edge < 50:
                dot.set_food_eaten(dot.food_eaten - 0.1
                )
                print(f"Dot {dot.id} is near an edge. Food eaten: {dot.food_eaten}")

        # Separate alive and dead dots
        alive_dots = [d for d in self.dots if d.food_eaten > 0]
        dead_dots = [d for d in self.dots if d.food_eaten <= 0]

        # Mark food_when_died for newly dead
        for d in dead_dots:
            if self.all_dots_record[d.id]["food_when_died"] is None:
                self.all_dots_record[d.id]["food_when_died"] = round(d.food_eaten, 2)
                print(f"Dot {d.id} has died. Food when died: {d.food_eaten}")

        self.dots = alive_dots

        new_dot_ids = set(d.id for d in self.dots)
        vanished_dot_ids = old_dot_ids - new_dot_ids
        for vid in vanished_dot_ids:
            if self.all_dots_record[vid]["food_when_died"] is None:
                dot_ref = self.all_dots_record[vid]["dot"]
                self.all_dots_record[vid]["food_when_died"] = round(dot_ref.food_eaten, 2)
                print(f"Dot {vid} has vanished. Food when died: {dot_ref.food_eaten}")

        self.dots_updated.emit()
        self.update()

        if self.current_step >= self.steps_per_generation:
            print("Reached steps per generation. Ending generation.")
            self.end_generation()

    def create_random_population(self, num_dots, birth_gen):
        population = []
        for _ in range(num_dots):
            x = random.randint(0, self.width() - 1)
            y = random.randint(0, self.height() - 1)
            speed = random.uniform(1, 3)
            dot = Dot(x, y, speed, birth_generation=birth_gen)
            self.all_dots_record[dot.id] = {"dot": dot, "food_when_died": None}
            population.append(dot)
        print(f"Created a random population of {len(population)} dots.")
        return population

    def end_generation(self):
        best_dots = self.algorithm.evaluate_fitness(self.dots)
        best_fitness = best_dots[0].food_eaten if best_dots else 0
        print(f"Best fitness of generation {self.algorithm.generation}: {best_fitness}")

        # Increment generation first
        self.algorithm.generation += 1
        print(f"Incremented to generation {self.algorithm.generation}")

        # Log data
        self.log_generation_data(best_fitness)

        # Produce the next generation
        new_dots = self.algorithm.next_generation(self.dots)
        if len(new_dots) == 0:
            print("No new generation produced. Creating random population.")
            new_dots = self.create_random_population(self.algorithm.population_size, self.algorithm.generation)

        # Assign birth_generation to new offspring
        for d in new_dots:
            d.birth_generation = self.algorithm.generation
            if d.id not in self.all_dots_record:
                self.all_dots_record[d.id] = {"dot": d, "food_when_died": None}
                print(f"Added new dot {d.id} to all_dots_record.")

        self.dots = new_dots
        self.current_step = 0

        # Clear existing food and add a new cluster
        self.clear_food()
        center_x = self.width() // 2
        center_y = self.height() // 2
        for _ in range(50):
            fx = random.randint(center_x - 50, center_x + 50)
            fy = random.randint(center_y - 50, center_y + 50)
            self.foods.append(Food(fx, fy))
        print(f"Added 50 new food items in the center for generation {self.algorithm.generation}.")

        self.generation_updated.emit(self.algorithm.generation, best_fitness)
        print(f"Generation {self.algorithm.generation} ended and updated.")

    def log_generation_data(self, best_fitness):
        print("Logging generation data.")
        for dot_id, rec in self.all_dots_record.items():
            dot = rec["dot"]
            lifetime = (self.algorithm.generation - dot.birth_generation) * self.steps_per_generation
            status = "Alive" if dot in self.dots else "Dead"
            food_when_died = rec["food_when_died"] if status == "Dead" else None

            self.experiment_data.append({
                "generation": self.algorithm.generation,
                "dot_id": dot.id,
                "food_eaten": round(dot.food_eaten, 2),
                "highest_food": round(dot.max_food_eaten, 2),
                "food_when_died": food_when_died,
                "lifetime_steps": lifetime,
                "status": status,
                "generation_created": dot.birth_generation
            })

        self.write_to_csv()

    def write_to_csv(self):
        fieldnames = ["generation", "dot_id", "food_eaten", "highest_food", "food_when_died", "lifetime_steps", "status", "generation_created"]
        try:
            with open(self.output_csv, 'x', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                print(f"Created new CSV file: {self.output_csv}")
        except FileExistsError:
            pass

        with open(self.output_csv, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for record in self.experiment_data:
                writer.writerow(record)
            print(f"Wrote {len(self.experiment_data)} records to CSV.")
            self.experiment_data = []

    def clear_food(self):
        self.foods = []
        self.update()
        print("Cleared all food from the board.")

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
            points = [
                QPoint(int(food.x), int(food.y)),
                QPoint(int(food.x + 10), int(food.y)),
                QPoint(int(food.x + 5), int(food.y - 10))
            ]
            painter.drawPolygon(*points)
