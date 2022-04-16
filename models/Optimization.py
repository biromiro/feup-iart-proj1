import itertools
import random
import math


class Optimization:
    @staticmethod
    def simulated_annealing(state, schedule, adaptive=False):
        temp = 1000
        fsi = state.evaluate()
        f = fsi
        for t in itertools.count(start=1):
            if adaptive:
                temp = schedule(temp, t, fsi, f)
            else:
                temp = schedule(temp, t)

            if round(temp, 4) == 0:
                return state

            next_state = state.random_neighbour()
            val1 = next_state.evaluate()
            val2 = state.evaluate()
            delta = val1 - val2
            if delta < 0:
                state = next_state
                fsi = state.evaluate()
                if(f > fsi):
                    f = fsi
            else:
                valueToCompare = random.random()
                probability = math.exp(-float(delta) / temp)
                if probability > valueToCompare:
                    state = next_state
                    fsi = state.evaluate()
                    if(f > fsi):
                        f = fsi
