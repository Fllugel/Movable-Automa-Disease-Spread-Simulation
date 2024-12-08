import math
import numpy as np
from cell_manager import CellManager

class Grid:
    def __init__(self, width, height, num_cells, infected_count, cell_speed, infection_probability, infection_display_duration, infection_distance, infection_period, cell_size):
        self.width = width
        self.height = height
        self.num_cells = num_cells
        self.infected_count = infected_count
        self.cell_speed = cell_speed
        self.infection_probability = infection_probability
        self.infection_display_duration = infection_display_duration
        self.infection_distance = infection_distance
        self.infection_period = infection_period
        self.cell_size = cell_size
        self.grid_size = int(np.ceil(np.sqrt(num_cells)))  # Define grid size based on number of cells
        self.cell_manager = CellManager(width, height, self.grid_size, cell_size, infection_display_duration, infection_period)
        self.min_distance = self.calculate_min_distance()

    def calculate_min_distance(self):
        # Calculate a dynamic minimum distance based on field size and cell count
        area_per_cell = (self.width * self.height) / self.num_cells
        return math.sqrt(area_per_cell) / 2

    def create_cells(self, num_cells, infected_count, cell_speed):
        self.cell_manager.create_cells(num_cells, infected_count, cell_speed)

    def update(self):
        self.cell_manager.update_cells(self.infection_distance, self.infection_probability, self.infection_period)

    def draw(self, screen, offset_x=0):
        self.cell_manager.draw_cells(screen, offset_x)