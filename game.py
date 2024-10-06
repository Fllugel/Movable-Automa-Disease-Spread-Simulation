import pygame
from grid import Grid


class Game:
    def __init__(self, width, height, num_cells):
        self.width = width
        self.height = height
        self.num_cells = num_cells
        self.grid = Grid(width, height, num_cells)
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.grid.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Clear the screen with black
        self.grid.draw(screen)
        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw(pygame.display.get_surface())
            clock.tick(60)
