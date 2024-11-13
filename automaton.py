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

class Cell:
    def __init__(self, x, y, speed, infected=False, size=3, latent=False):
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)
        self.infected = infected
        self.latent = latent
        self.infection_time = 0
        self.recovered = False
        self.dead = False
        self.speed = speed
        self.size = size

    def move(self, width, height):
        if self.dead:
            return  # Мертві клітини не рухаються

        # Плавна зміна швидкості
        self.speed_x += random.uniform(-SPEED_CHANGE_FACTOR, SPEED_CHANGE_FACTOR)
        self.speed_y += random.uniform(-SPEED_CHANGE_FACTOR, SPEED_CHANGE_FACTOR)

        # Обмежуємо максимальну швидкість
        self.speed_x = max(-MAX_SPEED, min(self.speed_x, MAX_SPEED))
        self.speed_y = max(-MAX_SPEED, min(self.speed_y, MAX_SPEED))

        self.x += self.speed_x
        self.y += self.speed_y

        # Відштовхування від стін
        if self.x <= 0 or self.x >= width:
            self.speed_x = -self.speed_x
        if self.y <= 0 or self.y >= height:
            self.speed_y = -self.speed_y

        # Обмеження, щоб точки не виходили за межі вікна
        self.x = max(0, min(self.x, width))
        self.y = max(0, min(self.y, height))

    def infect(self):
        if not self.infected and not self.latent:
            self.infected = True
            self.latent = True  # Спочатку клітина стає латентною

    def update_infection(self, death_probability):
        if self.infected:
            if self.latent:
                # Латентні клітини мають шанс стати активними
                if random.random() < LATENT_TO_ACTIVE_PROBABILITY:
                    self.latent = False  # Переходить в активний стан
            else:
                # Активні клітини можуть вмирати з певною ймовірністю
                if random.random() < death_probability:
                    self.dead = True
                    self.infected = False  # Завершуємо інфекцію
                # Активна клітина залишається активною, якщо не помирає

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
                    if other.state == CellState.HEALTHY:
                        self._attempt_infection(cell, other)

    def _attempt_infection(self, infected, other):
        distance = math.sqrt((infected.x - other.x) ** 2 + (infected.y - other.y) ** 2)
        if distance < self.infection_radius:
            if random.random() < self.infection_probability:
                other.state = CellState.LATENT
                self.daily_statistics["infected"] += 1

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