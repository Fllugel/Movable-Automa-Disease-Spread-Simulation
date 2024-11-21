import random
import pygame
from collections import defaultdict
from cell import Cell
from cell_state import CellState
from config import Config

class Automaton:
    def __init__(self, config: Config):
        self.width = 600
        self.height = 400
        self.cells = [Cell(random.randint(0, self.width), random.randint(0, self.height), config.cell_speed, size=config.cell_size, infection_period=config.infection_period) for _ in range(config.cell_count)]
        for i in range(config.infected_count):
            self.cells[i].transition_to_active()
        for i in range(round(config.cell_count * config.latent_prob)):
            self.cells[i + config.infected_count].transition_to_latent()

        self.infection_probability = config.infection_probability
        self.infection_radius = config.infection_radius
        self.death_probability = config.death_probability
        self.infection_check_timer = defaultdict(lambda: -float('inf'))
        self.running = True
        self.latent_to_active_prob = config.latent_to_active_prob
        self.infection_prob_latent = config.infection_prob_latent
        self.infection_prob_healthy = config.infection_prob_active
        self.daily_statistics = {"infected": 0, "dead": 0}
        self.infection_checks_per_day = 0.05
        self.infection_radii = []
        self.show_radius = True
        self.update_counter = 0
        self.color_healthy = config.color_healthy
        self.color_latent = config.color_latent
        self.color_active = config.color_active
        self.color_dead = config.color_dead
        self.background_color = config.background_color

    def update(self):
        if not self.running:
            return

        for cell in self.cells:
            cell.move(self.width, self.height)

        self.update_counter += 1
        if self.update_counter <= 1:
            for cell in self.cells:
                cell.update_infection(self.death_probability, self.latent_to_active_prob)

        if self.update_counter >= 1 / self.infection_checks_per_day:
            self.update_counter = 0
            self.check_if_can_infect()

    def check_if_can_infect(self):
        for cell in self.cells:
            if cell.state == CellState.ACTIVE:
                for other_cell in self.cells:
                    if cell.can_infect(other_cell, self.infection_radius):
                        other_cell.infect(self.infection_prob_healthy, self.infection_prob_latent)
                        self.infection_radii.append((cell, self.infection_radius, 255))

    def draw(self, screen, background_color):
        screen.fill(background_color)
        for cell in self.cells:
            if cell.state == CellState.DEAD:
                color = self.color_dead
            elif cell.state == CellState.LATENT:
                color = self.color_latent
            elif cell.state == CellState.ACTIVE:
                color = self.color_active
            else:
                color = self.color_healthy
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
        infected = len([c for c in self.cells if c.state == CellState.ACTIVE])
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
        if all(cell.state != CellState.ACTIVE for cell in self.cells):
            self.running = False