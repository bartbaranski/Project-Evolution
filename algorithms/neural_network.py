# algorithms/neural_network.py
import math
import random

class SimpleNeuralNetwork:
    def __init__(self, input_size=7, hidden_size=8, output_size=2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.w1 = [[random.uniform(-1,1) for _ in range(input_size)] for _ in range(self.hidden_size)]
        self.b1 = [random.uniform(-1,1) for _ in range(self.hidden_size)]
        
        self.w2 = [[random.uniform(-1,1) for _ in range(self.hidden_size)] for _ in range(self.output_size)]
        self.b2 = [random.uniform(-1,1) for _ in range(self.output_size)]

    def forward(self, inputs):
        hidden = []
        for i in range(self.hidden_size):
            val = sum(inputs[j]*self.w1[i][j] for j in range(self.input_size)) + self.b1[i]
            hidden.append(math.tanh(val))
        
        output = []
        for i in range(self.output_size):
            val = sum(hidden[j]*self.w2[i][j] for j in range(self.hidden_size)) + self.b2[i]
            output.append(math.tanh(val))
        return output

    def mutate(self, rate=0.1):
        def mutate_val(val):
            if random.random() < 0.1:
                return val + random.uniform(-rate, rate)
            return val
        
        for i in range(self.hidden_size):
            for j in range(self.input_size):
                self.w1[i][j] = mutate_val(self.w1[i][j])
            self.b1[i] = mutate_val(self.b1[i])
        
        for i in range(self.output_size):
            for j in range(self.hidden_size):
                self.w2[i][j] = mutate_val(self.w2[i][j])
            self.b2[i] = mutate_val(self.b2[i])

    def copy(self):
        new_net = SimpleNeuralNetwork(self.input_size, self.hidden_size, self.output_size)
        new_net.w1 = [row[:] for row in self.w1]
        new_net.b1 = self.b1[:]
        new_net.w2 = [row[:] for row in self.w2]
        new_net.b2 = self.b2[:]
        return new_net

    @staticmethod
    def crossover(parent1, parent2):
        child = parent1.copy()
        crossover_point = random.randint(1, parent1.hidden_size - 1)
        for i in range(crossover_point, parent1.hidden_size):
            child.w1[i] = parent2.w1[i][:]
            child.b1[i] = parent2.b1[i]

        crossover_point2 = random.randint(1, parent1.output_size - 1)
        for i in range(crossover_point2, parent1.output_size):
            child.w2[i] = parent2.w2[i][:]
            child.b2[i] = parent2.b2[i]

        return child
