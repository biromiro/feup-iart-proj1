import random
from src.model.Direction import Direction

class Mutation:
    @staticmethod
    def mutate_percent(percentage, mutator):
        if random.randrange(100) >= percentage:
            return lambda offspring: offspring
        else:
            return mutator
    
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
        offspring.commands[index] = Direction.random()
        return offspring

    @staticmethod
    def swap_side(offspring):
        index = random.randrange(len(offspring.commands)-1)
        aux = offspring.commands[index]
        offspring.commands[index] = offspring.commands[index+1]
        offspring.commands[index+1] = aux
        return offspring