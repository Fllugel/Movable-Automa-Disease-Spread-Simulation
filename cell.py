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
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Collision with walls
        if self.x < 0 or self.x > width:
            self.direction = (-self.direction[0], self.direction[1])  # Reverse horizontal direction
        if self.y < 0 or self.y > height:
            self.direction = (self.direction[0], -self.direction[1])  # Reverse vertical direction

    def draw(self, screen, offset_x=0):
        # Change color based on infection status
        color = (255, 0, 0) if self.infected else self.color
        pygame.draw.circle(screen, color, (self.x + offset_x, self.y), self.radius)

    def check_collision(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return distance < (self.radius + other.radius)

    def handle_collision(self, other):
        if self.check_collision(other):
            # Calculate the normal vector at the collision point
            normal = (other.x - self.x, other.y - self.y)
            normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
            normal = (normal[0] / normal_length, normal[1] / normal_length)  # Normalize the normal vector

            # Calculate the dot product of the direction vectors
            dot_product_self = self.direction[0] * normal[0] + self.direction[1] * normal[1]
            dot_product_other = other.direction[0] * normal[0] + other.direction[1] * normal[1]

            # Reflect the directions based on the normal vector
            self.direction = (
                self.direction[0] - 2 * dot_product_self * normal[0],
                self.direction[1] - 2 * dot_product_self * normal[1]
            )
            other.direction = (
                other.direction[0] - 2 * dot_product_other * normal[0],
                other.direction[1] - 2 * dot_product_other * normal[1]
            )

            # Infect the other cell if one is infected
            if self.infected and not other.infected:
                other.infected = True
            elif other.infected and not self.infected:
                self.infected = True
