import itertools
import random
import math
its = 0


class Optimization:
    """Optimization algorithms."""

    @staticmethod
    def simulated_annealing(state, schedule, adaptive=False, temp=1000, use_preferred_moves=False):
        """Simulated annealing. The algorithm yields the states on every iteration."""
        fsi = state.evaluate()
        f = fsi
        for t in itertools.count(start=1):
            yield state
            if adaptive:
                temp = schedule(temp, t, fsi, f)
            else:
                temp = schedule(temp, t)

            if round(temp, 5) == 0: # Stop condition
                return

            if state.board.preferred_moves and use_preferred_moves:
                next_state = state.preferred_moves_neighbour()
            else:
                next_state = state.random_neighbour()

            val1 = next_state.evaluate()
            val2 = state.evaluate()
            delta = val1 - val2
            if delta < 0: # better solution found
                state = next_state
                fsi = state.evaluate()
                if f > fsi:
                    f = fsi
            else: # worse state. accept with probability based on temperature
                valueToCompare = random.random()
                probability = math.exp(-float(delta) / temp)
                if probability > valueToCompare:
                    state = next_state
                    fsi = state.evaluate()
                    if f > fsi:
                        f = fsi

    @staticmethod
    def genetic_algorithms(gen_zero, selector, crosser, mutator, terminator, hold_best=None):
        """Genetic algorithms. This algorithm yields the fittest in every generation."""
        gen_size = len(gen_zero)
        cur_generation = gen_zero
        next_generation = []

        def fittest(generation):
            """Returns the fittest individual in the generation."""
            best = None
            for individual in generation:
                fitness = individual.evaluate()
                if not best or fitness < best[1]:
                    best = (individual, fitness)
            return best[0]

        yield fittest(cur_generation)
        while not terminator(cur_generation): # terminator is the stop condition
            for _ in range(gen_size):
                parent1, parent2 = selector(cur_generation)
                offspring = crosser(parent1, parent2)
                offspring = mutator(offspring)
                next_generation.append(offspring)
            
            if hold_best: # hold the best to the next generation
                cur_generation = hold_best(cur_generation) + next_generation
            else:
                cur_generation = next_generation

            yield fittest(cur_generation)
            next_generation = []
