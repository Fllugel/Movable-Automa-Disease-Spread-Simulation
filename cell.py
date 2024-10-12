import pygame
import random
import math


class Cell:
    def __init__(self, x, y, color=(255, 255, 255), radius=5, infected=False, speed=2):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speed = speed
        angle = random.uniform(0, 2 * math.pi)
        self.direction = (math.cos(angle), math.sin(angle))
        self.infected = infected

    def move(self, width, height):
        if self.speed != 0:
            # Introduce a small random change in direction
            angle_change = random.uniform(-0.1, 0.1)
            new_direction_x = self.direction[0] * math.cos(angle_change) - self.direction[1] * math.sin(angle_change)
            new_direction_y = self.direction[0] * math.sin(angle_change) + self.direction[1] * math.cos(angle_change)

            # Normalize the new direction
            length = math.sqrt(new_direction_x ** 2 + new_direction_y ** 2)
            self.direction = (new_direction_x / length, new_direction_y / length)

            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed

        # Collision with walls
        if self.x < 0 or self.x > width:
            self.direction = (-self.direction[0], self.direction[1])  # Reverse horizontal direction
            self.x = max(0, min(self.x, width))  # Reposition within bounds
        if self.y < 0 or self.y > height:
            self.direction = (self.direction[0], -self.direction[1])  # Reverse vertical direction
            self.y = max(0, min(self.y, height))  # Reposition within bounds

    def draw(self, screen, offset_x=0):
        # Change color based on infection status
        color = (255, 0, 0) if self.infected else self.color
        pygame.draw.circle(screen, color, (self.x + offset_x, self.y), self.radius)

    def handle_infection(self, other, infection_distance, infection_probability):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        if distance < infection_distance:
            if random.random() < infection_probability:
                if self.infected and not other.infected:
                    other.infected = True
                elif other.infected and not self.infected:
                    self.infected = True