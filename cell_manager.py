import random
import time
from cell import Cell
from cell_state import CellState  # Add this import

class CellManager:
    def __init__(self, width, height, grid_size, cell_size, infection_display_duration, infection_period):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.infection_display_duration = infection_display_duration
        self.infection_period = infection_period
        self.cells = []
        self.cell_grid = [[[] for _ in range(grid_size)] for _ in range(grid_size)]

    def create_cells(self, num_cells, infected_count, cell_speed):
        self.cells.clear()
        self.cell_grid = [[[] for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for _ in range(num_cells):
            self.add_cell(cell_speed)

        for i in random.sample(range(num_cells), infected_count):
            self.cells[i].state = CellState.INFECTED
            self.cells[i].infection_start_time = time.time()

    def add_cell(self, speed):
        while True:
            new_x = random.randint(0, self.width - 1)
            new_y = random.randint(0, self.height - 1)
            new_cell = Cell(new_x, new_y, speed=speed, infection_display_duration=self.infection_display_duration, size=self.cell_size, infection_period=self.infection_period)

            grid_x = min(int(new_x / self.width * self.grid_size), self.grid_size - 1)
            grid_y = min(int(new_y / self.height * self.grid_size), self.grid_size - 1)

            self.cells.append(new_cell)
            self.cell_grid[grid_x][grid_y].append(new_cell)
            break

    def update_cells(self, infection_distance, infection_probability, infection_period):
        for i, cell in enumerate(self.cells):
            cell.move(self.width, self.height)

            if cell.state == CellState.INFECTED and time.time() - cell.infection_start_time > infection_period:
                cell.state = CellState.RECOVERED

            for other in self.cells[i + 1:]:
                cell.handle_infection(other, infection_distance=infection_distance, infection_probability=infection_probability)


    def draw_cells(self, screen, offset_x=0):
        for cell in self.cells:
            cell.draw(screen, offset_x)