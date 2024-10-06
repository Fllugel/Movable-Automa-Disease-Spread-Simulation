import pygame
import sys
from grid import Grid

# Game settings
WIDTH = 800  # Width of the window
HEIGHT = 600  # Height of the window
NUM_CELLS = 100  # Total number of cells
INFECTED_COUNT = 10  # Number of initially infected cells
CELL_SPEED = 1  # Speed of cell movement

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cellular Automaton - Infection Simulation")

    # Create the grid with specified settings
    grid = Grid(WIDTH, HEIGHT, NUM_CELLS, infected_count=INFECTED_COUNT)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid.update()

        screen.fill((0, 0, 0))  # Clear the screen
        grid.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
