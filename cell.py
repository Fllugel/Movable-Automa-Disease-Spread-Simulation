import math
import random
import time

import pygame

from cell_state import CellState


def _generate_random_direction():
    angle = random.uniform(0, 2 * math.pi)
    return math.cos(angle), math.sin(angle)


class Cell:
    def __init__(self, x, y, speed, infection_display_duration, size=5):
        self.x = x
        self.y = y
        self.speed = speed
        self.infection_display_duration = infection_display_duration
        self.size = size
        self.radius = size // 2
        self.state = CellState.SUSCEPTIBLE
        self.infection_radius = 0
        self.last_infection_check = 0
        self.infection_alpha = 255
        self.direction = _generate_random_direction()

    def move(self, width, height):
        if self.speed != 0:
            self._update_direction()
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            self._handle_boundaries(width, height)

    def _update_direction(self):
        angle_change = random.uniform(-0.1, 0.1)
        new_direction_x = self.direction[0] * math.cos(angle_change) - self.direction[1] * math.sin(angle_change)
        new_direction_y = self.direction[0] * math.sin(angle_change) + self.direction[1] * math.cos(angle_change)
        length = math.sqrt(new_direction_x ** 2 + new_direction_y ** 2)
        self.direction = (new_direction_x / length, new_direction_y / length)

    def _handle_boundaries(self, width, height):
        if self.x < 0 or self.x > width:
            self.direction = (-self.direction[0], self.direction[1])
            self.x = max(0, min(self.x, width))
        if self.y < 0 or self.y > height:
            self.direction = (self.direction[0], -self.direction[1])
            self.y = max(0, min(self.y, height))

    def draw(self, screen, offset_x=0):
        color = (255, 0, 0) if self.state == CellState.INFECTED else (255, 255, 255)
        pygame.draw.circle(screen, color, (self.x + offset_x, self.y), self.radius)
        self._draw_infection_radius(screen, offset_x)

    def _draw_infection_radius(self, screen, offset_x):
        time_since_check = time.time() - self.last_infection_check
        if time_since_check < self.infection_display_duration:
            self.infection_alpha = max(0, 255 - int((time_since_check / self.infection_display_duration) * 255))
            infection_radius_surface = pygame.Surface((max(1, self.infection_radius * 2), max(1, self.infection_radius * 2)),
                                                      pygame.SRCALPHA)
            pygame.draw.circle(infection_radius_surface, (0, 255, 0, self.infection_alpha),
                               (self.infection_radius, self.infection_radius), self.infection_radius, 1)
            screen.blit(infection_radius_surface,
                        (self.x + offset_x - self.infection_radius, self.y - self.infection_radius))

    def handle_infection(self, other, infection_distance, infection_probability):
        if self.state != CellState.INFECTED or other.state != CellState.SUSCEPTIBLE:
            return

        distance = self._calculate_distance(other)
        if distance < infection_distance:
            self.last_infection_check = time.time()
            self.infection_radius = infection_distance
            self.infection_alpha = 255
            if random.random() < infection_probability:
                other.state = CellState.INFECTED

    def _calculate_distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)