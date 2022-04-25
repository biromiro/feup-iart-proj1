class Termination:
    """Termination conditions for the genetic algorithm."""

    def __init__(self):
        self.iteration = 0

    @staticmethod
    def optimal(solution_size):
        """Terminate only after find a solution of the given size."""
        def has_optimal(generation):
            for individual in generation:
                if individual.evaluate() == solution_size:
                    return True
            return False
        return has_optimal

    def iteration_cap(self, cap):
        """Terminate after a given number of iterations."""
        def reached_cap(generation):
            if self.iteration == cap:
                return True
            self.iteration += 1
            return False
        return reached_cap
