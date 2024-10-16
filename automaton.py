import random
import pygame
import math
from collections import defaultdict

WHITE = (127, 179, 213)  # Здоровий (блакитний)
GREEN = (66, 66, 66)     # Видужав (темно-сірий)
RED = (241, 148, 138)    # Заражений (червоний)
BACKGROUND_DARK = (0, 0, 0)  # Темний фон для гри
BACKGROUND_LIGHT = (255, 255, 255)  # Світлий фон для гри

class Cell:
    def __init__(self, x, y, speed, infected=False):
        self.x = x
        self.y = y
        self.speed_x = random.uniform(-speed, speed)
        self.speed_y = random.uniform(-speed, speed)
        self.infected = infected
        self.infection_time = 0
        self.recovered = False
        self.speed = speed

    def move(self, width, height):
        self.speed_x += random.uniform(-0.05, 0.05)  # Легка зміна швидкості
        self.speed_y += random.uniform(-0.05, 0.05)

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

    def update_infection(self, infection_period):
        if self.infected:
            self.infection_time += 1
            if self.infection_time >= infection_period:
                self.infected = False
                self.recovered = True

class Automaton:
    def __init__(self, width, height, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period):
        self.width = width
        self.height = height
        self.cells = [Cell(random.randint(0, width), random.randint(0, height), cell_speed) for _ in range(cell_count)]
        for i in range(infected_count):
            self.cells[i].infected = True

        self.infection_probability = infection_probability
        self.infection_radius = infection_radius
        self.infection_period = infection_period
        self.radius_animation_phase = 0
        self.radius_to_draw = []  # Список для клітин, де малюємо радіус
        self.infection_check_timer = defaultdict(lambda: -float('inf'))  # Таймер для перевірок інфікування

    def update(self):
        self.radius_animation_phase = (self.radius_animation_phase + 1) % 120
        self.radius_to_draw.clear()
        for cell in self.cells:
            cell.move(self.width, self.height)
            cell.update_infection(self.infection_period)

        self.infect()

    def infect(self):
        for cell in self.cells:
            if cell.infected:
                for other in self.cells:
                    if not other.infected and not other.recovered:
                        dist = math.hypot(cell.x - other.x, cell.y - other.y)
                        if dist < self.infection_radius:
                            key = (id(cell), id(other))  # Унікальний ключ для кожної пари клітин
                            if pygame.time.get_ticks() - self.infection_check_timer[key] > 1000:  # Таймер в 1 сек.
                                self.radius_to_draw.append(cell)
                                self.infection_check_timer[key] = pygame.time.get_ticks()  # Оновлення таймера
                                if random.random() < self.infection_probability:
                                    other.infected = True

    def draw(self, screen, background_color):
        screen.fill(background_color)
        for cell in self.cells:
            if cell.recovered:
                color = GREEN
            elif cell.infected:
                color = RED
            else:
                color = WHITE
            pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), 3)

        # Малюємо радіус зараження для клітин, де була перевірка ймовірності зараження
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for cell in self.radius_to_draw:
            opacity = max(0, 80 - math.sin(self.radius_animation_phase / 60 * math.pi) * 80)
            animated_radius = self.infection_radius + math.sin(self.radius_animation_phase / 60 * math.pi) * 10
            color_with_opacity = (241, 148, 138)
            pygame.draw.circle(surface, color_with_opacity, (int(cell.x), int(cell.y)), int(animated_radius), 1)
            surface.set_alpha(int(opacity))
        screen.blit(surface, (0, 0))

    def get_statistics(self):
        healthy = len([c for c in self.cells if not c.infected and not c.recovered])
        infected = len([c for c in self.cells if c.infected])
        recovered = len([c for c in self.cells if c.recovered])
        return healthy, infected, recovered
