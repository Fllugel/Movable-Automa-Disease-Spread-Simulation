from cell import Cell
import random
import math
import numpy as np

class Grid:
    def __init__(self, width, height, num_cells, infected_count=5, cell_speed=2, infection_probability=0.1, infection_display_duration=1, infection_distance=20, cell_size=5):
        self.width = width
        self.height = height
        self.cells = []
        self.infected_count = infected_count
        self.cell_speed = cell_speed
        self.num_cells = num_cells
        self.infection_probability = infection_probability
        self.infection_display_duration = infection_display_duration
        self.infection_distance = infection_distance
        self.cell_size = cell_size
        self.grid_size = int(np.ceil(np.sqrt(num_cells)))  # Define grid size based on number of cells
        self.cell_grid = [[[] for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.min_distance = self.calculate_min_distance()

    def calculate_min_distance(self):
        # Calculate a dynamic minimum distance based on field size and cell count
        area_per_cell = (self.width * self.height) / self.num_cells
        return math.sqrt(area_per_cell) / 2

    def create_cells(self, num_cells, infected_count, cell_speed):
        self.cells.clear()
        self.cell_grid = [[[] for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for _ in range(num_cells):
            self.add_cell(cell_speed)

        for i in random.sample(range(num_cells), infected_count):
            self.cells[i].set_infected()

    def add_cell(self, speed):
        while True:
            new_x = random.randint(0, self.width - 1)
            new_y = random.randint(0, self.height - 1)
            new_cell = Cell(new_x, new_y, speed=speed, infection_display_duration=self.infection_display_duration, size=self.cell_size)

            grid_x = min(int(new_x / self.width * self.grid_size), self.grid_size - 1)
            grid_y = min(int(new_y / self.height * self.grid_size), self.grid_size - 1)

            self.cells.append(new_cell)
            self.cell_grid[grid_x][grid_y].append(new_cell)
            break

    def update(self):
        for i, cell in enumerate(self.cells):
            cell.move(self.width, self.height)
            for other in self.cells[i + 1:]:
                cell.handle_infection(other, infection_distance=self.infection_distance, infection_probability=self.infection_probability)

    def draw(self, screen, offset_x=0):
        for cell in self.cells:
            cell.draw(screen, offset_x)