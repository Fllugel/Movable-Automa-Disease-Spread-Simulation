from enum import Enum

class CellState(Enum):
    HEALTHY = 1
    LATENT = 2
    INFECTED = 3
    DEAD = 4