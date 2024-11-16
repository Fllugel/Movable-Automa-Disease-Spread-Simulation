import random
import pygame
from collections import defaultdict
from cell import Cell
from cell_state import CellState

BLUE = (127, 179, 213)
PURPLE = (255, 140, 255)
PINK = (255, 100, 100)
BLACK = (0, 0, 0)
BACKGROUND_DARK = (0, 0, 0)
BACKGROUND_LIGHT = (255, 255, 255)

class Automaton:
    def __init__(self, width, height, cell_count, infected_count, latent_count, cell_speed, infection_probability, infection_radius, infection_period, death_probability, cell_size, latent_to_active_prob, infection_prob_latent, infection_prob_healthy):
        self.width = width
        self.height = height
        self.cells = [Cell(random.randint(0, width), random.randint(0, height), cell_speed, size=cell_size, infection_period=infection_period) for _ in range(cell_count)]
        for i in range(infected_count):
            self.cells[i].become_infected()
        for i in range(round(cell_count * latent_count)):
            self.cells[i + infected_count].become_latent()

        self.infection_probability = infection_probability
        self.infection_radius = infection_radius
        self.death_probability = death_probability
        self.infection_check_timer = defaultdict(lambda: -float('inf'))
        self.running = True
        self.latent_to_active_prob = latent_to_active_prob
        self.infection_prob_latent = infection_prob_latent
        self.infection_prob_healthy = infection_prob_healthy
        self.daily_statistics = {"infected": 0, "dead": 0}
        self.infection_checks_per_day = 0.05
        self.infection_radii = []
        self.show_radius = True
        self.update_counter = 0

    def update(self):
        if not self.running:
            return

        for cell in self.cells:
            cell.move(self.width, self.height)

        self.update_counter += 1
        if self.update_counter <= 1:
            self.check_infected()

        if self.update_counter >= 1 / self.infection_checks_per_day:
            self.update_counter = 0
            self.check_if_can_infect()


    def check_infected(self):
        for cell in self.cells:
            cell.update_infection(self.death_probability, self.latent_to_active_prob)

    def check_if_can_infect(self):
        for cell in self.cells:
            if cell.state == CellState.INFECTED:
                for other_cell in self.cells:
                    if other_cell.state in [CellState.HEALTHY, CellState.LATENT]:
                        distance = ((cell.x - other_cell.x) ** 2 + (cell.y - other_cell.y) ** 2) ** 0.5
                        if distance <= self.infection_radius:
                            self.infect(other_cell)
                            self.infection_radii.append((cell, self.infection_radius, 255))

    def infect(self, other_cell):
        if other_cell.state == CellState.HEALTHY:
            infection_probability = self.infection_prob_healthy
        elif other_cell.state == CellState.LATENT:
            infection_probability = self.infection_prob_latent
        else:
            return

        if random.random() < infection_probability:
            other_cell.become_infected()
        else:
            other_cell.become_latent()

    def draw(self, screen, background_color):
        screen.fill(background_color)
        for cell in self.cells:
            if cell.state == CellState.DEAD:
                color = BLACK
            elif cell.state == CellState.LATENT:
                color = PURPLE
            elif cell.state == CellState.INFECTED:
                color = PINK
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), cell.size)

        if self.show_radius:
            for i, (cell, radius, alpha) in enumerate(self.infection_radii):
                if alpha > 0:
                    surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pygame.draw.circle(surface, (255, 0, 0, alpha), (int(cell.x), int(cell.y)), int(radius), 1)
                    screen.blit(surface, (0, 0))
                    self.infection_radii[i] = (cell, radius, alpha - 15)

            self.infection_radii = [r for r in self.infection_radii if r[2] > 0]

    def get_statistics(self):
        healthy = len([c for c in self.cells if c.state == CellState.HEALTHY])
        infected = len([c for c in self.cells if c.state == CellState.INFECTED])
        latent = len([c for c in self.cells if c.state == CellState.LATENT])
        dead = len([c for c in self.cells if c.state == CellState.DEAD])
        return healthy, infected, latent, dead

    def reset_daily_statistics(self):
        daily_stats = self.daily_statistics.copy()
        self.daily_statistics = {"infected": 0, "dead": 0}
        return daily_stats

    @staticmethod
    def update_current_day(current_day):
        Cell.current_day = current_day

    def stop_if_no_infected(self):
        if all(cell.state != CellState.INFECTED for cell in self.cells):
            self.running = False

    def toggle_radii(self):
        self.show_radius = not self.show_radius