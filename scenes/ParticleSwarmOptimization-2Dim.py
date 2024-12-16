import math
import random
from typing import Tuple, List

# Constants
VELOCITY_BOUNDS: Tuple[float, float] = (0, 1) # R_1 & R_2
INERTIA: float = 1                      # w
DIMENSION: int = 2

# Hyperparameters
SWARM_POPULATION: int = 100
MAX_ITERATIONS: int = 10                 # n
BOUNDS: Tuple[float, float] = (-5, 5)
COGNITIVE_COEFFICIENT: float = 1      # C_1
SOCIAL_COEFFICIENT: float = 0.5         # C_2

def fitness_function(x: float, y: float) -> float:
    return math.cos(2 * x + y) + math.pow(x - y, 2) - 5 * x + 3 * y + 2

# Implementation
class Particle:
    def __init__(self, pos: List[float], fitness_value: float, velocity: List[float]):
        self.pos = pos
        self.fitness_value = fitness_value
        self.velocity = velocity
        self.best_pos = pos.copy()

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

def main() -> None:
    swarm = Swarm(SWARM_POPULATION)

    for iteration in range(MAX_ITERATIONS):
        for (i, particle) in enumerate(swarm.particles):
            print("Particle {} position: {}".format(i, particle.pos))

            for dim in range(DIMENSION):
                particle.velocity[dim] = (
                    INERTIA * particle.velocity[dim] +
                    COGNITIVE_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (particle.best_pos[dim] - particle.pos[dim]) +
                    SOCIAL_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (swarm.best_pos[dim] - particle.pos[dim])
                )

                particle.pos[dim] += particle.velocity[dim]
                particle.pos[dim] = max(BOUNDS[0], min(particle.pos[dim], BOUNDS[1])) # Make sure particle stays inside given dimension's boundaries

            particle.fitness_value = fitness_function(particle.pos[0], particle.pos[1])

            if particle.fitness_value < fitness_function(particle.best_pos[0], particle.best_pos[1]):
                particle.best_pos = particle.pos.copy()

                if particle.fitness_value < swarm.best_fitness_value:
                    swarm.best_pos = particle.pos.copy()
                    swarm.best_fitness_value = particle.fitness_value
        print("-----------------------------")

    print("G_best: {}".format(swarm.best_pos))

if __name__ == "__main__":
    main()