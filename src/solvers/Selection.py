import random
from src.solvers.State import State
from src.model.Direction import Direction


class Selection:
    """Selection for the genetic algorithm."""

    @staticmethod
    def generation_zero(population_size, solution_size, board):
        """Creates a generation with the given population and solution size."""
        gen_zero = []
        for _ in range(population_size):
            individual = State([], board)
            for _ in range(solution_size):
                individual.commands.append(Direction.random())
            gen_zero.append(individual)
        return gen_zero

    @staticmethod
    def best_n(cap):
        """Select the best cap individuals from the generation."""
        def elite_selector(gen):
            return sorted(gen, key=lambda x: x.evaluate())[:cap]
        return elite_selector

    @staticmethod
    def elitist(cut):
        """Randomly select two parents from the best cut of the generation."""
        def elite_selector(generation):
            last_admission = int(len(generation)*cut)
            elite = sorted(generation, key=lambda individual: individual.evaluate())[
                :last_admission]
            return (random.choice(elite), random.choice(elite))
        return elite_selector

    @staticmethod
    def random_parents(generation):
        """Select two random parents from the generation."""
        return Selection.elitist(1)(generation)

    @staticmethod
    def roulette(generation):
        """Roulette selection."""

        # Calculate total fitness and fitnesses
        total_fitness = 0
        fitnesses = []
        for individual in generation:
            fitness = individual.evaluate()
            fitnesses.append(fitness)
            total_fitness += fitness

        # Roll two random numbers
        roll1 = 0
        roll2 = 0
        if total_fitness > 0:
            roll1 = random.randrange(total_fitness)
            roll2 = random.randrange(total_fitness)
        
        # Select parents from the fitness roulette based on rolls
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
