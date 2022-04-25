import random
from src.solvers.State import State
from src.model.Direction import Direction


class Selection:
    @staticmethod
    def generation_zero(population_size, solution_size, board):
        gen_zero = []
        for _ in range(population_size):
            individual = State([], board)
            for _ in range(solution_size):
                individual.commands.append(Direction.random())
            gen_zero.append(individual)
        return gen_zero

    @staticmethod
    def best_n(cap):
        def elite_selector(gen):
            return sorted(gen, key=lambda x: x.evaluate())[:cap]
        return elite_selector

    @staticmethod
    def elitist(cut):
        def elite_selector(generation):
            last_admission = int(len(generation)*cut)
            elite = sorted(generation, key=lambda individual: individual.evaluate())[
                :last_admission]
            return (random.choice(elite), random.choice(elite))
        return elite_selector

    @staticmethod
    def random_parents(generation):
        return Selection.elitist(1)(generation)

    @staticmethod
    def roulette(generation):
        total_fitness = 0
        fitnesses = []
        for individual in generation:
            fitness = individual.evaluate()
            fitnesses.append(fitness)
            total_fitness += fitness

        roll1 = random.randrange(total_fitness)
        roll2 = random.randrange(total_fitness)
        parent1 = None
        parent2 = None
        for individual, fitness in zip(generation, fitnesses):
            if not parent1:
                roll1 -= fitness
                if roll1 <= 0:
                    parent1 = individual
            if not parent2:
                roll2 -= fitness
                if roll2 <= 0:
                    parent2 = individual

            if parent1 and parent2:
                return (parent1, parent2)
