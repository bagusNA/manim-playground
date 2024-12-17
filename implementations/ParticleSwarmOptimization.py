import math
import random
from typing import Tuple, List

from matplotlib import pyplot as plt


# Hyperparameters
VELOCITY_BOUNDS: Tuple[float, float] = (0, 1) # R_1 & R_2
INERTIA: float = 1                      # w

SWARM_POPULATION: int = 10
MAX_ITERATIONS: int = 3                 # n
BOUNDS: Tuple[float, float] = (0, 5)
COGNITIVE_COEFFICIENT: float = 0.5      # C_1
SOCIAL_COEFFICIENT: float = 1         # C_2

def fitness_function(x: float) -> float:
    return math.pow((7 * x - 3), 2) + math.exp((1 / 2) * math.pow(x, 2))

# Implementation
class Particle:
    def __init__(self, pos: float, fitness_value: float, velocity: float):
        self._pos: float = pos
        self.pos_history: List[float] = [pos]

        self._fitness_value: float = fitness_value
        self.fitness_value_history: List[float] = [fitness_value]

        self.velocity: float = velocity
        self.best_pos: float = pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self.pos_history.append(value)

    @property
    def fitness_value(self):
        return self._fitness_value

    @fitness_value.setter
    def fitness_value(self, value):
        self._fitness_value = value
        self.fitness_value_history.append(value)


class Swarm:
    def __init__(self, population):
        self.particles: List[Particle] = []
        self.best_pos: float | None = None                  # G_best
        self.best_fitness_value: float = math.inf

        # Generate particles
        for i in range(population):
            pos = round(random.uniform(*BOUNDS), 5)

            particle = Particle(
                pos = pos,
                fitness_value = fitness_function(pos),
                velocity = 0
            )

            self.particles.append(particle)

            if (self.best_pos is None) or (particle.fitness_value < self.best_fitness_value):
                self.best_pos = particle.pos
                self.best_fitness_value = particle.fitness_value

class PSO:
    def __init__(self):
        self.swarm = Swarm(SWARM_POPULATION)

    def run(self):
        for iteration in range(MAX_ITERATIONS):
            print("--- Iterasi {} ---".format(iteration + 1))

            for (i, particle) in enumerate(self.swarm.particles):
                particle.velocity = (
                        INERTIA * particle.velocity +
                        COGNITIVE_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (
                                    particle.best_pos - particle.pos) +
                        SOCIAL_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (
                                    self.swarm.best_pos - particle.pos)
                )

                particle.pos = max(BOUNDS[0], min(particle.pos + particle.velocity, BOUNDS[1]))  # Make sure particle stays inside given boundaries

                particle.fitness_value = fitness_function(particle.pos)

                if particle.fitness_value < fitness_function(particle.best_pos):
                    particle.best_pos = particle.pos

                    if particle.fitness_value < self.swarm.best_fitness_value:
                        self.swarm.best_pos = particle.pos
                        self.swarm.best_fitness_value = particle.fitness_value

                print("Particle {}".format(i + 1))
                print(
                    "      x: {}, fitness: {}, velocity: {}, p_best: {}"
                    .format(round(particle.pos, 4), round(particle.fitness_value, 4), round(particle.velocity, 4), round(particle.best_pos, 4))
                )

            print("G_best: {}".format(round(self.swarm.best_pos, 4)))
            print("")

        print("G_best: {}".format(round(self.swarm.best_pos, 4)))
        print("Best Fitness: {}".format(round(self.swarm.best_fitness_value, 4)))

if __name__ == '__main__':
    pso = PSO()
    pso.run()

    fig, (pos_plot, fitness_plot) = plt.subplots(2)

    for particle in pso.swarm.particles:
        pos_plot.plot(particle.pos_history, '-o')
        fitness_plot.plot(particle.fitness_value_history, '-o')

    pos_plot.set_ylabel('x')
    pos_plot.set_xlabel('Iterasi')

    fitness_plot.set_ylabel('f(x)')
    fitness_plot.set_xlabel('Iterasi')
    fitness_plot.set_ylim([0, 100])

    fig.suptitle("Perkembangan Partikel Selama Iterasi")

    # plt.show()

    # with tempconfig({ 'output_file': 'a.png' }):
    #     pos_plot = PSOPosPlot(pso, MAX_ITERATIONS, BOUNDS)
    #     pos_plot.render()
    #
    # fitness_plot = PSOFitnessPlot(pso, MAX_ITERATIONS)
    # fitness_plot.render()