import pygame

class Panel:
    def __init__(self, width, height, grid):
        self.width = width
        self.height = height
        self.grid = grid

        self.cell_count_input_box = pygame.Rect(width // 2 - 75, 70, 150, 30)
        self.infected_count_input_box = pygame.Rect(width // 2 - 75, 110, 150, 30)
        self.cell_speed_input_box = pygame.Rect(width // 2 - 75, 150, 150, 30)
        self.infection_probability_input_box = pygame.Rect(width // 2 - 75, 190, 150, 30)
        self.infection_radius_input_box = pygame.Rect(width // 2 - 75, 230, 150, 30)

        self.color_inactive = pygame.Color(255, 255, 255)
        self.color_active = pygame.Color(200, 200, 200)

        self.cell_count_color = self.color_inactive
        self.infected_count_color = self.color_inactive
        self.cell_speed_color = self.color_inactive
        self.infection_probability_color = self.color_inactive
        self.infection_radius_color = self.color_inactive

        self.active_cell_count = False
        self.active_infected_count = False
        self.active_cell_speed = False
        self.active_infection_probability = False
        self.active_infection_radius = False

        self.cell_count_text = str(grid.num_cells)
        self.infected_count_text = str(grid.infected_count)
        self.cell_speed_text = str(grid.cell_speed)
        self.infection_probability_text = "0.1"
        self.infection_radius_text = str(grid.infection_distance)

        pygame.font.init()
        self.font = pygame.font.Font(None, 20)

        self.button = pygame.Rect(width // 2 - 50, height - 80, 100, 40)
        self.button_color = (0, 128, 255)
        self.button_hover_color = (0, 100, 200)
        self.button_text = 'Start'

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cell_count_input_box.collidepoint(event.pos):
                self.active_cell_count = not self.active_cell_count
                self.active_infected_count = False
                self.active_cell_speed = False
                self.active_infection_probability = False
                self.active_infection_radius = False
            elif self.infected_count_input_box.collidepoint(event.pos):
                self.active_infected_count = not self.active_infected_count
                self.active_cell_count = False
                self.active_cell_speed = False
                self.active_infection_probability = False
                self.active_infection_radius = False
            elif self.cell_speed_input_box.collidepoint(event.pos):
                self.active_cell_speed = not self.active_cell_speed
                self.active_cell_count = False
                self.active_infected_count = False
                self.active_infection_probability = False
                self.active_infection_radius = False
            elif self.infection_probability_input_box.collidepoint(event.pos):
                self.active_infection_probability = not self.active_infection_probability
                self.active_cell_count = False
                self.active_infected_count = False
                self.active_cell_speed = False
                self.active_infection_radius = False
            elif self.infection_radius_input_box.collidepoint(event.pos):
                self.active_infection_radius = not self.active_infection_radius
                self.active_cell_count = False
                self.active_infected_count = False
                self.active_cell_speed = False
                self.active_infection_probability = False
            else:
                self.active_cell_count = False
                self.active_infected_count = False
                self.active_cell_speed = False
                self.active_infection_probability = False
                self.active_infection_radius = False

            self.cell_count_color = self.color_active if self.active_cell_count else self.color_inactive
            self.infected_count_color = self.color_active if self.active_infected_count else self.color_inactive
            self.cell_speed_color = self.color_active if self.active_cell_speed else self.color_inactive
            self.infection_probability_color = self.color_active if self.active_infection_probability else self.color_inactive
            self.infection_radius_color = self.color_active if self.active_infection_radius else self.color_inactive

            if self.button.collidepoint(event.pos):
                try:
                    num_cells = int(self.cell_count_text) if self.cell_count_text.isdigit() else self.grid.num_cells
                    infected_count = int(self.infected_count_text) if self.infected_count_text.isdigit() else self.grid.infected_count
                    cell_speed = int(self.cell_speed_text) if self.cell_speed_text.isdigit() else self.grid.cell_speed
                    infection_probability = float(self.infection_probability_text) if self.infection_probability_text.replace('.', '', 1).isdigit() else 0.1
                    infection_radius = int(self.infection_radius_text) if self.infection_radius_text.isdigit() else self.grid.infection_distance

                    self.grid.create_cells(num_cells, infected_count=infected_count, cell_speed=cell_speed)
                    self.grid.infection_probability = infection_probability
                    self.grid.infection_distance = infection_radius
                except ValueError:
                    print("Invalid input. Please enter a number!")

        if event.type == pygame.KEYDOWN:
            if self.active_cell_count:
                if event.key == pygame.K_BACKSPACE:
                    self.cell_count_text = self.cell_count_text[:-1]
                else:
                    self.cell_count_text += event.unicode
            elif self.active_infected_count:
                if event.key == pygame.K_BACKSPACE:
                    self.infected_count_text = self.infected_count_text[:-1]
                else:
                    self.infected_count_text += event.unicode
            elif self.active_cell_speed:
                if event.key == pygame.K_BACKSPACE:
                    self.cell_speed_text = self.cell_speed_text[:-1]
                else:
                    self.cell_speed_text += event.unicode
            elif self.active_infection_probability:
                if event.key == pygame.K_BACKSPACE:
                    self.infection_probability_text = self.infection_probability_text[:-1]
                else:
                    self.infection_probability_text += event.unicode
            elif self.active_infection_radius:
                if event.key == pygame.K_BACKSPACE:
                    self.infection_radius_text = self.infection_radius_text[:-1]
                else:
                    self.infection_radius_text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, self.width, self.height))

        # Title
        title_font = pygame.font.Font(None, 30)
        title_surface = title_font.render("Parameters panel", True, (255, 255, 255))
        screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 20))

        # List of parameters for input boxes
        input_labels = ["Cell Count", "Infected Count", "Cell Speed", "Infection Probability", "Infection Radius"]
        input_boxes = [
            (self.cell_count_input_box, self.cell_count_color, self.cell_count_text),
            (self.infected_count_input_box, self.infected_count_color, self.infected_count_text),
            (self.cell_speed_input_box, self.cell_speed_color, self.cell_speed_text),
            (self.infection_probability_input_box, self.infection_probability_color, self.infection_probability_text),
            (self.infection_radius_input_box, self.infection_radius_color, self.infection_radius_text)
        ]

        spacing = 10
        current_y = 70

        # Drawing text and boxes, then spacing them correctly
        for (box, color, text), label in zip(input_boxes, input_labels):
            # Text
            instructions_surface = self.font.render(label, True, (255, 255, 255))
            screen.blit(instructions_surface, (self.width // 2 - instructions_surface.get_width() // 2, current_y))

            current_y += instructions_surface.get_height() + spacing

            # Input box
            box.y = current_y
            txt_surface = self.font.render(text, True, color)
            text_x = box.x + 5
            text_y = box.y + (box.height - txt_surface.get_height()) // 2
            screen.blit(txt_surface, (text_x, text_y))
            pygame.draw.rect(screen, color, box, 2)

            current_y += box.height + spacing

        # Button
        mouse_pos = pygame.mouse.get_pos()
        if self.button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.button_hover_color, self.button)
        else:
            pygame.draw.rect(screen, self.button_color, self.button)

        button_text_surface = self.font.render(self.button_text, True, (255, 255, 255))
        screen.blit(button_text_surface, (self.button.x + (self.button.width - button_text_surface.get_width()) // 2,
                                          self.button.y + (self.button.height - button_text_surface.get_height()) // 2))