import itertools
import random
import math


class Optimization:
    @staticmethod
    def simulated_annealing(state, schedule, adaptive=False, use_preferred_moves=False):
        temp = 1000
        fsi = state.evaluate()
        f = fsi
        for t in itertools.count(start=1):
            yield state
            if adaptive:
                temp = schedule(temp, t, fsi, f)
            else:
                temp = schedule(temp, t)

            if round(temp, 4) == 0:
                return

            if state.board.preferred_moves and use_preferred_moves:
                next_state = state.preferred_moves_neighbour()
            else:
                next_state = state.random_neighbour()

            val1 = next_state.evaluate()
            val2 = state.evaluate()
            delta = val1 - val2
            if delta < 0:
                state = next_state
                fsi = state.evaluate()
                if f > fsi:
                    f = fsi
            else:
                valueToCompare = random.random()
                probability = math.exp(-float(delta) / temp)
                if probability > valueToCompare:
                    state = next_state
                    fsi = state.evaluate()
                    if f > fsi:
                        f = fsi

    @staticmethod
    def genetic_algorithms(gen_zero, selector, crosser, mutator, terminator):
        gen_size = len(gen_zero)
        cur_generation = gen_zero
        next_generation = []

        def fittest(generation):
            best = None
            for individual in generation:
                fitness = individual.evaluate()
                if not best or fitness < best[1]:
                    best = (individual, fitness)
            return best[0]
        
        while not terminator(cur_generation):
            print("new generation")
            for _ in range(gen_size):
                parent1, parent2 = selector(cur_generation)
                offspring = crosser(parent1, parent2)
                offspring = mutator(offspring)
                next_generation.append(offspring)
            cur_generation = next_generation
        
        return fittest(cur_generation)
            