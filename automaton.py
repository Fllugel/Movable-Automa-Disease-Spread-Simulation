
import random
import pygame
import math
from collections import defaultdict

BLUE = (127, 179, 213)  # Здоровий (блакитний)
GRAY = (66, 66, 66)     # Видужав (темно-сірий)
LATENT_RED = (255, 100, 100)  # Колір для латентної форми хвороби
ACTIVE_RED = (255, 0, 0)      # Яскравіший червоний для активної форми
BLACK = (0, 0, 0)        # Помер (чорний)
BACKGROUND_DARK = (0, 0, 0)  # Темний фон для гри
BACKGROUND_LIGHT = (255, 255, 255)  # Світлий фон для гри

MAX_SPEED = 2.0  # Максимальна швидкість для клітин
SPEED_CHANGE_FACTOR = 0.01  # Коефіцієнт для плавної зміни швидкості

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

    def update_infection(self, death_probability, latent_to_active_probability):
        if self.infected:
            if self.latent:
                # Латентні клітини мають шанс стати активними
                if random.random() < latent_to_active_probability:
                    self.latent = False  # Переходить в активний стан
            else:
                # Активні клітини можуть вмирати з певною ймовірністю
                if random.random() < death_probability:
                    self.dead = True
                    self.infected = False  # Завершуємо інфекцію

class Automaton:
    def __init__(self, width, height, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period, death_probability, cell_size,
                 latent_to_active_prob, infection_prob_latent, infection_prob_active):
        self.width = width
        self.height = height
        self.cells = [Cell(random.randint(0, width), random.randint(0, height), cell_speed, size=cell_size) for _ in range(cell_count)]
        for i in range(infected_count):
            self.cells[i].infected = True  # Initialize the first infected as active
            self.cells[i].latent = False

        self.infection_probability = infection_probability
        self.infection_radius = infection_radius
        self.infection_period = infection_period
        self.death_probability = death_probability
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
            if cell.infected:
                cell.update_infection(self.death_probability, self.latent_to_active_prob)
                if cell.dead:
                    self.daily_statistics["dead"] += 1

        self.infect()

    def infect(self):
        for cell in self.cells:
            if cell.infected and not cell.latent:  # Тільки активні клітини можуть заражати
                for other in self.cells:
                    if not other.infected and not other.recovered and not other.dead:
                        dist = math.hypot(cell.x - other.x, cell.y - other.y)
                        if dist < self.infection_radius:
                            key = (id(cell), id(other))
                            if pygame.time.get_ticks() - self.infection_check_timer[key] > 1000:
                                self.radius_to_draw.append(cell)
                                self.infection_check_timer[key] = pygame.time.get_ticks()
                                if random.random() < self.infection_probability:
                                    # Зараження як латентне або активне
                                    other.infected = True
                                    other.latent = random.random() < self.infection_prob_latent
                                    if not other.latent and random.random() < self.infection_prob_active:
                                        other.latent = False  # Стає активним одразу

    def draw(self, screen, background_color):
        screen.fill(background_color)
        for cell in self.cells:
            if cell.dead:
                color = BLACK
            elif cell.recovered:
                color = GRAY
            elif cell.infected:
                color = LATENT_RED if cell.latent else ACTIVE_RED
            else:
                color = BLUE
            pygame.draw.circle(screen, color, (int(cell.x), int(cell.y)), cell.size)

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for cell in self.radius_to_draw:
            color_with_opacity = (241, 148, 138)
            pygame.draw.circle(surface, color_with_opacity, (int(cell.x), int(cell.y)), int(self.infection_radius), 1)
        screen.blit(surface, (0, 0))

    def get_statistics(self):
        healthy = len([c for c in self.cells if not c.infected and not c.recovered and not c.dead])
        infected = len([c for c in self.cells if c.infected])
        latent = len([c for c in self.cells if c.latent])
        recovered = len([c for c in self.cells if c.recovered])
        dead = len([c for c in self.cells if c.dead])
        return healthy, infected, latent, recovered, dead

    def reset_daily_statistics(self):
        daily_stats = self.daily_statistics.copy()
        self.daily_statistics = {"infected": 0, "recovered": 0, "dead": 0}
        return daily_stats

    def stop_if_no_infected(self):
        if all(not cell.infected for cell in self.cells):
            self.running = False
