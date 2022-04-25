import random
from src.model.Direction import Direction


class Mutation:
    """Mutation functions for genetic algorithms."""

    @staticmethod
    def mutate_percent(percentage, mutator):
        """Mutates a percentage of the commands with the given mutator."""
        def occasional_mutator(offspring):
            val = random.randrange(100)
            if val > percentage:
                return offspring
            else:
                return mutator(offspring)
        return occasional_mutator

    @staticmethod
    def composite(mutators):
        """Composes a list of mutators."""
        def composite_mutator(offspring):
            for mutator in mutators:
                offspring = mutator(offspring)
            return offspring
        return composite_mutator

    @staticmethod
    def random_corruption(offspring):
        """Randomly ands removes or changes a command."""
        index = 0
        if len(offspring.commands) > 0:
            index = random.randrange(len(offspring.commands))
        choice = random.choice(['change', 'add', 'remove'])

        if len(offspring.commands) == 0: # can't remove or change commands on the empty list
            choice = 'add'

        if choice == 'change':
            offspring.commands[index] = Direction.random()
        elif choice == 'add':
            offspring.commands.insert(index, Direction.random())
        else:
            offspring.commands.pop(index)
        return offspring

    @staticmethod
    def swap_side(offspring):
        """Swaps a random command with the next one."""
        if len(offspring.commands) < 2: # can't swap 0 or 1 commands
            return offspring
        index = random.randrange(len(offspring.commands)-1) # command to swap with the next one
        aux = offspring.commands[index]
        offspring.commands[index] = offspring.commands[index+1]
        offspring.commands[index+1] = aux
        return offspring
