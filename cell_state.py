from enum import Enum

class CellState(Enum):
    HEALTHY = 1
    LATENT = 2
    INFECTED = 3
    RECOVERED = 4
    DEAD = 5