import pygame
import random
import math
import time
from cell_state import CellState

class Cell:
    def __init__(self, x, y, speed, infection_display_duration, size=5):
        self._x = x
        self._y = y
        self._speed = speed
        self._infection_display_duration = infection_display_duration
        self._size = size
        self._radius = size // 2
        self._state = CellState.SUSCEPTIBLE
        self._infection_radius = 0
        self._last_infection_check = 0
        self._infection_alpha = 255
        self._direction = self._generate_random_direction()

    def _generate_random_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        return (math.cos(angle), math.sin(angle))

    def move(self, width, height):
        if self._speed != 0:
            self._update_direction()
            self._x += self._direction[0] * self._speed
            self._y += self._direction[1] * self._speed
            self._handle_boundaries(width, height)

    def _update_direction(self):
        angle_change = random.uniform(-0.1, 0.1)
        new_direction_x = self._direction[0] * math.cos(angle_change) - self._direction[1] * math.sin(angle_change)
        new_direction_y = self._direction[0] * math.sin(angle_change) + self._direction[1] * math.cos(angle_change)
        length = math.sqrt(new_direction_x ** 2 + new_direction_y ** 2)
        self._direction = (new_direction_x / length, new_direction_y / length)

    def _handle_boundaries(self, width, height):
        if self._x < 0 or self._x > width:
            self._direction = (-self._direction[0], self._direction[1])
            self._x = max(0, min(self._x, width))
        if self._y < 0 or self._y > height:
            self._direction = (self._direction[0], -self._direction[1])
            self._y = max(0, min(self._y, height))

    def draw(self, screen, offset_x=0):
        color = (255, 0, 0) if self._state == CellState.INFECTED else (255, 255, 255)
        pygame.draw.circle(screen, color, (self._x + offset_x, self._y), self._radius)
        self._draw_infection_radius(screen, offset_x)

    def _draw_infection_radius(self, screen, offset_x):
        time_since_check = time.time() - self._last_infection_check
        if time_since_check < self._infection_display_duration:
            self._infection_alpha = max(0, 255 - int((time_since_check / self._infection_display_duration) * 255))
            infection_radius_surface = pygame.Surface((max(1, self._infection_radius * 2), max(1, self._infection_radius * 2)),
                                                      pygame.SRCALPHA)
            pygame.draw.circle(infection_radius_surface, (0, 255, 0, self._infection_alpha),
                               (self._infection_radius, self._infection_radius), self._infection_radius, 1)
            screen.blit(infection_radius_surface,
                        (self._x + offset_x - self._infection_radius, self._y - self._infection_radius))

    def handle_infection(self, other, infection_distance, infection_probability):
        if self._state != CellState.INFECTED or other._state != CellState.SUSCEPTIBLE:
            return

        distance = self._calculate_distance(other)
        if distance < infection_distance:
            self._last_infection_check = time.time()
            self._infection_radius = infection_distance
            self._infection_alpha = 255
            if random.random() < infection_probability:
                other.set_infected()

    def _calculate_distance(self, other):
        return math.sqrt((self._x - other._x) ** 2 + (self._y - other._y) ** 2)

    def is_infected(self):
        return self._state == CellState.INFECTED

    def set_infected(self):
        self._state = CellState.INFECTED

    def set_susceptible(self):
        self._state = CellState.SUSCEPTIBLE