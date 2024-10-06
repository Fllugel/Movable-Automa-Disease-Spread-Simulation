import pygame
from cell import Cell
import random
import math

class Grid:
    def __init__(self, width, height, num_cells, infected_count=5, cell_speed=2, min_distance=20):
        self.width = width
        self.height = height
        self.cells = []
        self.min_distance = min_distance

        for _ in range(num_cells):
            self.add_cell(cell_speed)

        # Randomly infect a subset of cells
        for i in random.sample(range(num_cells), infected_count):
            self.cells[i].infected = True

    def add_cell(self, speed):
        while True:
            new_x = random.randint(0, self.width)
            new_y = random.randint(0, self.height)
            new_cell = Cell(new_x, new_y, speed=speed)

            if all(self.is_far_enough(new_cell, other) for other in self.cells):
                self.cells.append(new_cell)
                break

    def is_far_enough(self, new_cell, other):
        distance = math.sqrt((new_cell.x - other.x) ** 2 + (new_cell.y - other.y) ** 2)
        return distance >= (new_cell.radius + other.radius + self.min_distance)

    def update(self):
        for i, cell in enumerate(self.cells):
            cell.move(self.width, self.height)
            for other in self.cells[i + 1:]:
                cell.handle_collision(other)

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)
