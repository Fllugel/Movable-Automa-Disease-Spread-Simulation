import random
import pygame
from collections import defaultdict
from cell import Cell
from cell_state import CellState

BLUE = (127, 179, 213)
GRAY = (66, 66, 66)
LATENT_RED = (255, 100, 100)
ACTIVE_RED = (255, 0, 0)
BLACK = (0, 0, 0)
BACKGROUND_DARK = (0, 0, 0)
BACKGROUND_LIGHT = (255, 255, 255)

class Automaton:
    def __init__(self, width, height, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period, death_probability, cell_size,
                 latent_to_active_prob, infection_prob_latent, infection_prob_active):
        self.width = width
        self.height = height
        self.cells = [Cell(random.randint(0, width), random.randint(0, height), cell_speed, size=cell_size) for _ in range(cell_count)]
        for i in range(infected_count):
            self.cells[i].state = CellState.INFECTED

        self.infection_probability = infection_probability
        self.infection_radius = infection_radius
        self.infection_period = infection_period
        self.death_probability = death_probability
        self.infection_check_timer = defaultdict(lambda: -float('inf'))
        self.running = True
        self.latent_to_active_prob = latent_to_active_prob
        self.infection_prob_latent = infection_prob_latent
        self.infection_prob_active = infection_prob_active
        self.infection_check_timer = defaultdict(lambda: -float('inf'))
        self.running = True
        self.daily_statistics = {"infected": 0, "dead": 0}

    def update(self):
        if not self.running:
            return

        for cell in self.cells:
            cell.move(self.width, self.height)
            if cell.state in [CellState.LATENT, CellState.INFECTED]:
                cell.update_infection(self.death_probability, self.latent_to_active_prob)


        self.check_if_can_infect()

    def check_if_can_infect(self):
        for cell in self.cells:
            if cell.state in [CellState.INFECTED, CellState.LATENT]:
                for other_cell in self.cells:
                    if other_cell.state == CellState.HEALTHY:
                        distance = ((cell.x - other_cell.x) ** 2 + (cell.y - other_cell.y) ** 2) ** 0.5
                        if distance <= self.infection_radius:
                            self.infect(other_cell)

    def infect(self, other_cell):
        if random.random() < self.infection_probability:
            other_cell.state = CellState.INFECTED

    def draw(self, screen, background_color):
        screen.fill(background_color)
        for cell in self.cells:
            if cell.state == CellState.DEAD:
                color = BLACK
            elif cell.state == CellState.LATENT:
                color = LATENT_RED
            elif cell.state == CellState.INFECTED:
                color = ACTIVE_RED
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), cell.size)

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        screen.blit(surface, (0, 0))

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

    def stop_if_no_infected(self):
        if all(cell.state != CellState.INFECTED for cell in self.cells):
            self.running = False