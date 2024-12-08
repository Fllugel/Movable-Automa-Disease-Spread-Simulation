import math
import random

import numpy as np
import pygame
from cell_state import CellState
from shapely.geometry import Polygon, Point


class Cell:
    MAX_SPEED = 2.0
    SPEED_CHANGE_FACTOR = 0.01

    def __init__(self, x, y, speed, size=3, infection_period=10):
        self._x = x
        self._y = y
        self._speed_x = random.uniform(-speed, speed)
        self._speed_y = random.uniform(-speed, speed)
        self._state = CellState.HEALTHY
        self._infection_start_day = -1
        self.speed = speed
        self.size = size
        self.infection_period = infection_period
        self.randomize_movement = True
        self._infection_alpha = 0

    # Properties for encapsulation
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = max(0, value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = max(0, value)

    @property
    def state(self):
        return self._state

    @property
    def infection_start_day(self):
        return self._infection_start_day

    def set_state(self, new_state):
        valid_transitions = {
            CellState.HEALTHY: [CellState.ACTIVE, CellState.LATENT],
            CellState.ACTIVE: [CellState.LATENT, CellState.DEAD],
            CellState.LATENT: [CellState.ACTIVE],
            CellState.DEAD: [],
        }
        if new_state not in valid_transitions[self._state]:
            raise ValueError(f"Invalid state transition: {self._state} to {new_state}")

        self._state = new_state

    def is_active(self):
        return self._state != CellState.DEAD

    def move(self, polygon: Polygon):
        if not self.is_active():
            return

        # Update speed with random changes if randomization is enabled
        if self.randomize_movement:
            self._speed_x += random.uniform(-self.SPEED_CHANGE_FACTOR, self.SPEED_CHANGE_FACTOR)
            self._speed_y += random.uniform(-self.SPEED_CHANGE_FACTOR, self.SPEED_CHANGE_FACTOR)

        # Clamp speed
        self._speed_x = max(-self.MAX_SPEED, min(self._speed_x, self.MAX_SPEED))
        self._speed_y = max(-self.MAX_SPEED, min(self._speed_y, self.MAX_SPEED))

        # Save old position
        old_x, old_y = self._x, self._y

        # Update position
        self._x += self._speed_x
        self._y += self._speed_y

        # Check if new position is within polygon
        if not polygon.contains(Point(self._x, self._y)):
            # Повертаємося до старої позиції
            self._x, self._y = old_x, old_y

            # Збереження поточної швидкості
            speed = math.sqrt(self._speed_x ** 2 + self._speed_y ** 2)

            # У 10% випадків додаємо випадкове збурення
            if random.random() < 0.2:
                self._speed_x += random.uniform(-0.5, 0.5)
                self._speed_y += random.uniform(-0.5, 0.5)

                # Нормалізація швидкості, щоб зберігати її постійною
                new_speed = math.sqrt(self._speed_x ** 2 + self._speed_y ** 2)
                self._speed_x *= speed / new_speed
                self._speed_y *= speed / new_speed
            else:
                # Стандартне відбиття
                self._speed_x = -self._speed_x
                self._speed_y = -self._speed_y

    def update_infection(self, death_probability, latent_to_active_probability, current_day):
        if self._state == CellState.LATENT:
            if random.random() < latent_to_active_probability:
                self.set_state(CellState.ACTIVE)
        elif self._state == CellState.ACTIVE:
            if current_day - self._infection_start_day >= self.infection_period:
                if random.random() < death_probability:
                    self.set_state(CellState.DEAD)
                else:
                    self.set_state(CellState.LATENT)
                    self._infection_start_day = -1

    def can_infect(self, other_cell, infection_radius):
        if self.state == CellState.ACTIVE and other_cell.state in [CellState.HEALTHY, CellState.LATENT]:
            distance = ((self.x - other_cell.x) ** 2 + (self.y - other_cell.y) ** 2) ** 0.5
            return distance <= infection_radius
        return False

    def infect(self, infection_prob_healthy, infection_prob_latent, infection_probability):
        if random.random() < infection_probability:
            if self.state == CellState.HEALTHY:
                if random.random() < infection_prob_healthy:
                    self.set_state(CellState.ACTIVE)
            elif self.state == CellState.LATENT:
                if random.random() < infection_prob_latent:
                    self.set_state(CellState.ACTIVE)

    def show_radius(self):
        self._infection_alpha = 255

    def draw(self, screen, color_healthy, color_latent, color_active, color_dead, show_radius, infection_radius, scale,
             offset_x, offset_y):
        if self.state == CellState.DEAD:
            color = color_dead
        elif self.state == CellState.LATENT:
            color = color_latent
        elif self.state == CellState.ACTIVE:
            color = color_active
        else:
            color = color_healthy

        # Ensure colors are consistent by converting them to the same format
        color = pygame.Color(*color)

        scaled_x = int(self.x * scale + offset_x)
        scaled_y = int(self.y * scale + offset_y)

        pygame.draw.circle(screen, color, (scaled_x, scaled_y), self.size * scale)

        if show_radius and self._infection_alpha > 0:
            surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 0, 0, self._infection_alpha), (scaled_x, scaled_y),
                               (infection_radius * scale), 1)
            screen.blit(surface, (0, 0))
            self._infection_alpha = max(0, self._infection_alpha - 10)


    @staticmethod
    def prob_contagiousness(day):
        contagiousness = (150, 90, 50, 0.5)
        in_con = 1
        l = in_con if in_con == 1 else in_con * 0.2  # Модифікований рівень контакту

        c, a, b, z = contagiousness
        if day <= c:
            x = (c - day) / a
            if x ** 2 <= 1:  # Перевірка на валідність виразу під коренем
                res = (1 - x ** 2) ** 0.5
            else:
                res = 0
        else:
            x = (day - c) / (b * (1 + (0.2 * (in_con - 1))))
            res = np.exp(-abs(x) ** 3)

        return res * z * l


    def calculate_infection_probability(self):
        day_of_infection = self.current_day - self._infection_start_day
        print(self, self.state, self._infection_start_day, self.prob_contagiousness(day_of_infection))
        return self.prob_contagiousness(day_of_infection)

