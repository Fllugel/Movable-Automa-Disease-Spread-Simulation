import pygame
import sys
from grid import Grid
from panel import Panel

# Game settings
WIDTH = 800  # Width of the window
HEIGHT = 600  # Height of the window
PANEL_WIDTH = 200
FPS = 60  # FPS CLOCK
INFECTION_DISPLAY_DURATION = 0.5  # Duration to show infection radius

# Panel basic values
NUM_CELLS = 100  # Total number of cells
INFECTED_COUNT = 10  # Number of initially infected cells
CELL_SPEED = 1  # Speed of cell movement
INFECTION_PROBABILITY = 0.1  # Basic infection probability
INFECTION_RADIUS = 20  # Basic infection radius

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH + PANEL_WIDTH, HEIGHT))
    pygame.display.set_caption("Cellular Automaton - Infection Simulation")

    # Create the grid with specified settings
    grid = Grid(WIDTH, HEIGHT, NUM_CELLS, infected_count=INFECTED_COUNT, cell_speed=CELL_SPEED, infection_probability=INFECTION_PROBABILITY, infection_distance=INFECTION_RADIUS, infection_display_duration=INFECTION_DISPLAY_DURATION)

    panel = Panel(PANEL_WIDTH, HEIGHT, grid)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            panel.handle_event(event)

        grid.update()

        screen.fill((0, 0, 0))  # Clear the screen
        panel.draw(screen)
        grid.draw(screen, PANEL_WIDTH)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()