# algorithms/evolution.py
import random

class EvolutionAlgorithm:
    def __init__(self):
        self.population_size = 20
        self.elite_size = 4
        self.generation = 1
        self.base_mutation_rate = 0.1
        self.mutation_rate = self.base_mutation_rate
        self.last_best_fitness = 0
        self.no_improvement_count = 0

    def evaluate_fitness(self, dots):
        return sorted(dots, key=lambda d: d.food_eaten, reverse=True)

    def roulette_wheel_selection(self, dots, count):
        total_fitness = sum(d.food_eaten for d in dots if d.food_eaten > 0)
        if total_fitness <= 0:
            print("Total fitness <= 0, selecting parents randomly.")
            return random.sample(dots, min(count, len(dots)))
        chosen = []
        for _ in range(count):
            pick = random.uniform(0, total_fitness)
            current = 0
            for d in dots:
                if d.food_eaten > 0:
                    current += d.food_eaten
                    if current >= pick:
                        chosen.append(d)
                        break
        print(f"Selected {len(chosen)} parents.")
        return chosen

    def reproduce_population(self, parents):
        from gui.board import Dot
        new_population = []
        top_performers = self.evaluate_fitness(parents)[:self.elite_size]
        new_population.extend(top_performers)
        print(f"Added top performers: {len(top_performers)}")

        # Use random.choices to allow parents to be selected multiple times
        while len(new_population) < self.population_size:
            if len(parents) == 0:
                print("No parents available for reproduction.")
                break
            # Allow selecting the same parent multiple times
            p1, p2 = random.choices(parents, k=2)
            child_net = p1.network.crossover(p1.network, p2.network)
            child_net.mutate(rate=self.mutation_rate)
            child_speed = p1.speed + random.uniform(-0.5, 0.5)
            child_speed = max(0.5, min(child_speed, 5.0))
            child = Dot(p1.x, p1.y, child_speed, network=child_net, birth_generation=0)  # birth_generation to be set later
            child.food_eaten = 5
            new_population.append(child)
            print(f"Reproduced new dot. Population size: {len(new_population)}")
        return new_population

    def next_generation(self, dots):
        ranked = self.evaluate_fitness(dots)
        best_fitness = ranked[0].food_eaten if ranked else 0
        print(f"Generation {self.generation} best fitness: {best_fitness}")

        if best_fitness <= self.last_best_fitness:
            self.no_improvement_count += 1
            print(f"No improvement. Count: {self.no_improvement_count}")
        else:
            self.no_improvement_count = 0
            self.last_best_fitness = best_fitness
            print("Improvement detected.")

        if self.no_improvement_count > 3:
            self.mutation_rate += 0.05
            print(f"No improvement for 4 generations. Increasing mutation rate to {self.mutation_rate}")
        else:
            self.mutation_rate = max(self.base_mutation_rate, self.mutation_rate - 0.01)
            print(f"Decreasing mutation rate to {self.mutation_rate}")

        if len(dots) == 0:
            print("No dots remain in the population.")
            return []

        requested_parents = max(self.elite_size*2, len(dots)//2)
        requested_parents = min(requested_parents, len(dots))
        print(f"Requested parents: {requested_parents}")

        if requested_parents <= 0:
            print("Requested parents <= 0. Skipping selection.")
            return []

        parents = self.roulette_wheel_selection(dots, requested_parents)
        if not parents:
            print("No parents were selected.")
            return []

        new_population = self.reproduce_population(parents)
        print(f"Next generation population size: {len(new_population)}")
        return new_population
