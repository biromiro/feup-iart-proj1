class Termination:
    def __init__(self):
        self.iteration = 0

    @staticmethod
    def optimal(solution_size):
        def has_optimal(generation):
            for individual in generation:
                val = individual.evaluate()
                if individual.evaluate() == solution_size:
                    return True
            return False
        return has_optimal

    def iteration_cap(self, cap):
        def reached_cap(generation):
            if self.iteration == cap:
                return True
            self.iteration += 1
            return False
        return reached_cap
