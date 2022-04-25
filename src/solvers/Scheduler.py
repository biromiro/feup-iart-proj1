import math


class Scheduler:
    """Schedulers for simulated annealing."""

    @staticmethod
    def linear_cooling(temperature, cycle=None, alpha=0.999):
        return temperature * alpha

    @staticmethod
    def exponential_multiplicative_cooling(temperature, cycle, alpha=0.999999):
        return temperature * alpha ** cycle

    @staticmethod
    def logarithmical_multiplicative_cooling(temperature, cycle, alpha=0.0001):
        return temperature / (1 + alpha * math.log(1 + cycle))

    @staticmethod
    def linear_multiplicative_cooling(temperature, cycle, alpha=0.000001):
        return temperature / (1 + alpha * cycle)

    @staticmethod
    def quadratic_multiplicative_cooling(temperature, cycle, alpha=0.000000001):
        return temperature / (1 + alpha * pow(cycle, 2))

    @staticmethod
    def adaptive_cooling(temperature, cycle, fsi, fstar):
        return Scheduler.exponential_multiplicative_cooling(temperature, cycle, 0.99999999) / (1 + (fsi - fstar) / fstar)
