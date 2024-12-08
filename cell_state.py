from enum import Enum

class CellState(Enum):
    HEALTHY = 1
    LATENT = 2
    ACTIVE = 3
    DEAD = 4