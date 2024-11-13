import random
import pygame
import math
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
        self.radius_animation_phase = 0
        self.radius_to_draw = []
        self.infection_check_timer = defaultdict(lambda: -float('inf'))
        self.running = True
        self.latent_to_active_prob = latent_to_active_prob
        self.infection_prob_latent = infection_prob_latent
        self.infection_prob_active = infection_prob_active
        self.radius_to_draw = []  # Список для клітин, де малюємо радіус
        self.infection_check_timer = defaultdict(lambda: -float('inf'))  # Таймер для перевірок інфікування
        self.running = True  # Статус симуляції
        self.daily_statistics = {"infected": 0, "recovered": 0, "dead": 0}

    def update(self):
        if not self.running:
            return

        self.radius_to_draw.clear()
        for cell in self.cells:
            cell.move(self.width, self.height)
            if cell.state in [CellState.LATENT, CellState.INFECTED]:
                cell.update_infection(self.death_probability)
                if cell.state == CellState.DEAD:
                    self.daily_statistics["dead"] += 1

        self.infect()

    def infect(self):
        for cell in self.cells:
            if cell.state == CellState.INFECTED:
                for other in self.cells:
                    if other.state not in [CellState.INFECTED, CellState.RECOVERED, CellState.DEAD]:
                        dist = math.hypot(cell.x - other.x, cell.y - other.y)
                        if dist < self.infection_radius:
                            key = (id(cell), id(other))
                            if pygame.time.get_ticks() - self.infection_check_timer[key] > 1000:
                                self.radius_to_draw.append(cell)
                                self.infection_check_timer[key] = pygame.time.get_ticks()
                                if random.random() < self.infection_probability:
                                    other.state = CellState.LATENT if random.random() < self.infection_prob_latent else CellState.INFECTED

    def draw(self, screen, background_color):
        screen.fill(background_color)
        for cell in self.cells:
            if cell.state == CellState.DEAD:
                color = BLACK
            elif cell.state == CellState.RECOVERED:
                color = GRAY
            elif cell.state == CellState.LATENT:
                color = LATENT_RED
            elif cell.state == CellState.INFECTED:
                color = ACTIVE_RED
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), cell.size)

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for cell in self.radius_to_draw:
            color_with_opacity = (241, 148, 138)
            pygame.draw.circle(surface, color_with_opacity, (int(cell.x), int(cell.y)), int(self.infection_radius), 1)
        screen.blit(surface, (0, 0))

    def get_statistics(self):
        healthy = len([c for c in self.cells if c.state == CellState.HEALTHY])
        infected = len([c for c in self.cells if c.state == CellState.INFECTED])
        latent = len([c for c in self.cells if c.state == CellState.LATENT])
        recovered = len([c for c in self.cells if c.state == CellState.RECOVERED])
        dead = len([c for c in self.cells if c.state == CellState.DEAD])
        return healthy, infected, latent, recovered, dead

    def reset_daily_statistics(self):
        daily_stats = self.daily_statistics.copy()
        self.daily_statistics = {"infected": 0, "recovered": 0, "dead": 0}
        return daily_stats

    def stop_if_no_infected(self):
        if all(cell.state != CellState.INFECTED for cell in self.cells):
            self.running = False