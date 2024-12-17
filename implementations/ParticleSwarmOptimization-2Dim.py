import math
import random
from typing import Tuple, List

# Constants
VELOCITY_BOUNDS: Tuple[float, float] = (0, 1) # R_1 & R_2
INERTIA: float = 1                      # w
DIMENSION: int = 2

# Hyperparameters
SWARM_POPULATION: int = 10
MAX_ITERATIONS: int = 3                 # n
BOUNDS: Tuple[float, float] = (-5, 5)
COGNITIVE_COEFFICIENT: float = 1      # C_1
SOCIAL_COEFFICIENT: float = 0.5         # C_2

def fitness_function(x: float, y: float) -> float:
    return math.cos(2 * x + y) + math.pow(x - y, 2) - 5 * x + 3 * y + 2

# Implementation
class Particle:
    def __init__(self, pos: List[float], fitness_value: float, velocity: List[float]):
        self._pos: List[float] = pos
        self.pos_history: List[List[float]] = [pos]

        self._fitness_value: float = fitness_value
        self.fitness_value_history: List[float] = [fitness_value]

        self.velocity = velocity
        self.best_pos = pos.copy()


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
        self.best_pos: List[float] | None = None                  # G_best
        self.best_fitness_value: float = math.inf

        # Generate particles
        for i in range(population):
            pos = [round(random.uniform(*BOUNDS), 5), round(random.uniform(*BOUNDS), 5)]

            particle = Particle(
                pos = pos,
                fitness_value = fitness_function(pos[0], pos[1]),
                velocity = [0, 0]
            )

            self.particles.append(particle)

            if (self.best_pos is None) or (particle.fitness_value < self.best_fitness_value):
                self.best_pos = particle.pos.copy()
                self.best_fitness_value = particle.fitness_value

class PSO:
    def __init__(self):
        self.swarm = Swarm(SWARM_POPULATION)

    def run(self) -> None:
        for iteration in range(MAX_ITERATIONS):
            print("--- Iterasi {} ---".format(iteration + 1))

            for (i, particle) in enumerate(self.swarm.particles):
                for dim in range(DIMENSION):
                    particle.velocity[dim] = (
                        INERTIA * particle.velocity[dim] +
                        COGNITIVE_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (particle.best_pos[dim] - particle.pos[dim]) +
                        SOCIAL_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (self.swarm.best_pos[dim] - particle.pos[dim])
                    )

                    particle.pos[dim] = max(BOUNDS[0], min(particle.pos[dim] + particle.velocity[dim], BOUNDS[1])) # Make sure particle stays inside given dimension's boundaries

                particle.fitness_value = fitness_function(particle.pos[0], particle.pos[1])

                if particle.fitness_value < fitness_function(particle.best_pos[0], particle.best_pos[1]):
                    particle.best_pos = particle.pos.copy()

                    if particle.fitness_value < self.swarm.best_fitness_value:
                        self.swarm.best_pos = particle.pos.copy()
                        self.swarm.best_fitness_value = particle.fitness_value

                print("Particle {}".format(i + 1))
                print(
                    "      x: {}, y: {}, fitness: {}, velocity_x: {}, velocity_y: {}, p_best_x: {}, p_best_y: {}"
                    .format(round(particle.pos[0], 4), round(particle.pos[1], 4), round(particle.fitness_value, 4), round(particle.velocity[0], 4), round(particle.velocity[1], 4), round(particle.best_pos[0], 4), round(particle.best_pos[1], 4))
                )

            print("G_best -> x: {}, y: {}".format(round(self.swarm.best_pos[0], 4), round(self.swarm.best_pos[1], 4)))
            print("")

        print("G_best -> x: {}, y: {}".format(round(self.swarm.best_pos[0], 4), round(self.swarm.best_pos[1], 4)))
        print("Best Fitness: {}".format(round(self.swarm.best_fitness_value, 4)))

if __name__ == "__main__":
    pso = PSO()
    pso.run()