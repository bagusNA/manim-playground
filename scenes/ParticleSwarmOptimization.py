import math
import random
from typing import Tuple, List

# Constants
VELOCITY_BOUNDS: Tuple[float, float] = (0, 1) # R_1 & R_2
INERTIA: float = 1                      # w

# Hyperparameters
SWARM_POPULATION: int = 100
MAX_ITERATIONS: int = 10                 # n
BOUNDS: Tuple[float, float] = (0, 5)
COGNITIVE_COEFFICIENT: float = 0.5      # C_1
SOCIAL_COEFFICIENT: float = 0.5         # C_2

def fitness_function(x: float) -> float:
    return math.pow((7 * x - 3), 2) + math.exp((1 / 2) * math.pow(x, 2))

# Implementation
class Particle:
    def __init__(self, pos: float, fitness_value: float, velocity: float):
        self.pos = pos
        self.fitness_value = fitness_value
        self.velocity = velocity
        self.best_pos = pos

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

def main() -> None:
    swarm = Swarm(SWARM_POPULATION)

    for iteration in range(MAX_ITERATIONS):
        for (i, particle) in enumerate(swarm.particles):
            print("Particle {} position: {}".format(i, particle.pos))

            particle.velocity = (
                    INERTIA * particle.velocity +
                    COGNITIVE_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (particle.best_pos - particle.pos) +
                    SOCIAL_COEFFICIENT * round(random.uniform(*VELOCITY_BOUNDS), 5) * (swarm.best_pos - particle.pos)
            )

            particle.pos += particle.velocity
            particle.pos = max(BOUNDS[0], min(particle.pos, BOUNDS[1])) # Make sure particle stays inside given boundaries

            particle.fitness_value = fitness_function(particle.pos)

            if particle.fitness_value < fitness_function(particle.best_pos):
                particle.best_pos = particle.pos

                if particle.fitness_value < swarm.best_fitness_value:
                    swarm.best_pos = particle.pos
                    swarm.best_fitness_value = particle.fitness_value
        print("-----------------------------")

    print("G_best: {}".format(swarm.best_pos))

if __name__ == "__main__":
    main()