import random
from collections import defaultdict
from cell import Cell
from cell_state import CellState
from config import Config

class CellAutomaton:
    def __init__(self, config: Config):
        self.config = config
        self.width = 600
        self.height = 400
        self.cells = self._initialize_cells()
        self.infection_check_timer = defaultdict(lambda: -float('inf'))
        self.running = True
        self.update_counter = 0
        self.daily_statistics = {"infected": 0, "dead": 0}
        self._initialize_colors()
        self.current_day = 0
        self.show_radius = False

    def _initialize_cells(self):
        cells = [Cell(random.randint(0, self.width), random.randint(0, self.height), self.config.cell_speed, size=self.config.cell_size, infection_period=self.config.infection_period) for _ in range(self.config.cell_count)]
        for i in range(self.config.infected_count):
            cells[i].set_state(CellState.ACTIVE)
        for i in range(round(self.config.cell_count * self.config.latent_prob)):
            cells[i + self.config.infected_count].set_state(CellState.LATENT)
        return cells

    def _initialize_colors(self):
        self.color_healthy = self.config.color_healthy
        self.color_latent = self.config.color_latent
        self.color_active = self.config.color_active
        self.color_dead = self.config.color_dead
        self.background_color = self.config.background_color

    def update(self, current_iteration, current_day):
        if not self.running:
            return

        self.current_day = current_day

        # Call _update_infections once a day
        if current_iteration % self.config.iterations_per_day == 0:
            self._update_infections()

        # Call _spread_infections infection_checks_per_day times a day
        if current_iteration % (self.config.iterations_per_day // self.config.infection_checks_per_day) == 0:
            self._spread_infections()

        self._move_cells()

    def _update_infections(self):
        for cell in self.cells:
            cell.update_infection(self.config.death_probability, self.config.latent_to_active_prob, self.current_day)

    def _move_cells(self):
        for cell in self.cells:
            cell.move(self.width, self.height)

    def _spread_infections(self):
        for cell in self.cells:
            for other_cell in self.cells:
                if cell.can_infect(other_cell, self.config.infection_radius):
                    other_cell.infect(self.config.infection_prob_healthy, self.config.infection_prob_latent, self.config.infection_probability, self.current_day)
                    cell.show_radius()


    def draw(self, screen):
        screen.fill(self.background_color)
        for cell in self.cells:
            cell.draw(screen, self.color_healthy, self.color_latent, self.color_active, self.color_dead, self.show_radius, self.config.infection_radius)

    def get_statistics(self):
        healthy = len([c for c in self.cells if c.state == CellState.HEALTHY])
        infected = len([c for c in self.cells if c.state == CellState.ACTIVE])
        latent = len([c for c in self.cells if c.state == CellState.LATENT])
        dead = len([c for c in self.cells if c.state == CellState.DEAD])
        return healthy, infected, latent, dead

    def reset_daily_statistics(self):
        daily_stats = self.daily_statistics.copy()
        self.daily_statistics = {"infected": 0, "dead": 0}
        return daily_stats

    def no_infected(self):
        return all(cell.state != CellState.ACTIVE for cell in self.cells)