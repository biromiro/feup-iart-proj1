import random
from src.solvers.State import State
from itertools import cycle


class Crossover:
    @staticmethod
    def random_origin(parent1, parent2):
        offspring = State([], parent1.board)
        p1_commands = parent1.commands
        p2_commands = parent2.commands

        if len(p1_commands) < len(p2_commands):
            p1_commands = cycle(p1_commands)
        else:
            p2_commands = cycle(p2_commands)

        for command1, command2 in zip(p1_commands, p2_commands):
            if random.getrandbits(1) and command1:
                offspring.commands.append(command1)
            else:
                offspring.commands.append(command2)
        return offspring

    @staticmethod
    def split(parent1, parent2):
        split_point = 0
        if len(parent1.commands) > 0:
            split_point = random.randrange(len(parent1.commands))
        offspring = State(
            parent1.commands[:split_point] + parent2.commands[split_point:], parent1.board)
        return offspring
