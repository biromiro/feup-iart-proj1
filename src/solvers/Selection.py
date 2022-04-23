import random

class Selection: 
    @staticmethod
    def elitist(cut):
        def elite_selector(generation):
            last_admission = len(generation)*cut
            elite = sorted(generation, key=lambda individual: individual.evaluate())[:last_admission]
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

        