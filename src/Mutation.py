import random
from src.Direction import Direction


class Mutation:
    @staticmethod
    def mutate_percent(percentage, mutator):
        def occasional_mutator(offspring):
            val = random.randrange(100)
            if val > percentage:
                return offspring
            else:
                return mutator(offspring)
        return occasional_mutator

    @staticmethod
    def composite(mutators):
        def composite_mutator(offspring):
            for mutator in mutators:
                offspring = mutator(offspring)
            return offspring
        return composite_mutator

    @staticmethod
    def random_corruption(offspring):
        index = random.randrange(len(offspring.commands))
        choice = random.choice(['change', 'add', 'remove'])

        if len(offspring.commands) == 0:
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
        index = random.randrange(len(offspring.commands)-1)
        aux = offspring.commands[index]
        offspring.commands[index] = offspring.commands[index+1]
        offspring.commands[index+1] = aux
        return offspring
