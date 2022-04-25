import random
from src.solvers.State import State

class Crossover:
    @staticmethod
    def random_origin(parent1, parent2):
        offspring = State([], parent1.board)
        for command1, command2 in zip(parent1.commands, parent2.commands):
            if random.getrandbits(1):
                offspring.commands.append(command1)
            else:
                offspring.commands.append(command2)
        return offspring