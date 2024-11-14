import random
from cell_state import CellState

MAX_SPEED = 2.0
SPEED_CHANGE_FACTOR = 0.01

class Cell:
    def __init__(self, x, y, speed, size=3):
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)
        self.state = CellState.HEALTHY
        self.infection_time = 0
        self.speed = speed
        self.size = size

    def move(self, width, height):
        if self.state == CellState.DEAD:
            return

        self.speed_x += random.uniform(-SPEED_CHANGE_FACTOR, SPEED_CHANGE_FACTOR)
        self.speed_y += random.uniform(-SPEED_CHANGE_FACTOR, SPEED_CHANGE_FACTOR)

        self.speed_x = max(-MAX_SPEED, min(self.speed_x, MAX_SPEED))
        self.speed_y = max(-MAX_SPEED, min(self.speed_y, MAX_SPEED))

        self.x += self.speed_x
        self.y += self.speed_y

        if self.x <= 0 or self.x >= width:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= height:
            self.speed_y = -self.speed_y

        self.x = max(0, min(self.x, width))
        self.y = max(0, min(self.y, height))

    def infect(self):
        if self.state == CellState.HEALTHY:
            self.state = CellState.LATENT

    def update_infection(self, death_probability, latent_to_active_probability):
        if self.state == CellState.LATENT:
            if random.random() < latent_to_active_probability:
                self.state = CellState.INFECTED
        elif self.state == CellState.INFECTED:
            if random.random() < death_probability:
                self.state = CellState.DEAD