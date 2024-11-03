import random



class EvolutionAlgorithm:
    def __init__(self):
        
        self.population_size = 100
        self.generations = 50

    def initialize_population(self):
        
        pass

    def evaluate_fitness(self):
        
        pass

    def selection(self):
        
        pass

    def crossover(self):
        
        pass  

    def mutation(self):
       
        pass

    def mutate(self, dot):
      
        dot.speed += random.uniform(-0.5, 0.5)
        if dot.speed < 0.5:
            dot.speed = 0.5
        elif dot.speed > 5:
            dot.speed = 5

    def run(self):
        
        self.initialize_population()
        for generation in range(self.generations):
            self.evaluate_fitness()
            self.selection()  
            self.crossover()  
            self.mutation()  
            
