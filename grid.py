import pygame
from cell import Cell
import random
import math

class Grid:
    def __init__(self, width, height, num_cells, infected_count=5, cell_speed=2, min_distance=20, infection_probability=0.1, infection_display_duration=1, infection_distance=20, cell_size=5):
        self.width = width
        self.height = height
        self.cells = []
        self.min_distance = min_distance
        self.infected_count = infected_count
        self.cell_speed = cell_speed
        self.num_cells = num_cells
        self.infection_probability = infection_probability
        self.infection_display_duration = infection_display_duration
        self.infection_distance = infection_distance
        self.cell_size = cell_size

    def create_cells(self, num_cells, infected_count, cell_speed):
        self.cells.clear()

        for _ in range(num_cells):
            self.add_cell(cell_speed)

        for i in random.sample(range(num_cells), infected_count):
            self.cells[i].infected = True

    def add_cell(self, speed):
        while True:
            new_x = random.randint(0, self.width)
            new_y = random.randint(0, self.height)
            new_cell = Cell(new_x, new_y, speed=speed, infection_display_duration=self.infection_display_duration, size=self.cell_size)

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
                cell.handle_infection(other, infection_distance=self.infection_distance, infection_probability=self.infection_probability)

    def draw(self, screen, offset_x=0):
        for cell in self.cells:
            cell.draw(screen, offset_x)