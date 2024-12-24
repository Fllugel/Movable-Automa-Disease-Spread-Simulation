import pygame
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QImage
from cell_automaton import CellAutomaton
from config import Config


class GameWidget(QWidget):
    statistics_updated = pyqtSignal(int, int, int, int, int)
    simulation_data_saved = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = None
        self.setFixedSize(600, 400)
        self._initialize_pygame()
        self.cell_automaton = None
        self.is_paused = False
        self.auto_stop_enabled = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)
        self.current_iteration = 0
        self.current_day = 0
        self.auto_stop_triggered = False
        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.polygon_points = []
        self.current_simulation = 0

    def _initialize_pygame(self):
        pygame.init()
        self.screen = pygame.Surface((600, 400))

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def toggle_auto_stop(self):
        self.auto_stop_enabled = not self.auto_stop_enabled


    def start_simulation(self, config: Config):
        self.cell_automaton = CellAutomaton(config)
        self.cell_automaton.offset_x = self.offset_x
        self.cell_automaton.offset_y = self.offset_y
        self.cell_automaton.scale = self.scale
        self.current_day = 0
        self.config = config
        self.is_paused = False

        self.auto_stop_triggered = False
        self.current_iteration = 0
        # self.current_simulation = 0

    def game_loop(self):
        if self.cell_automaton and not self.is_paused:
            self.current_iteration += 1

            if self.current_iteration % self.config.iterations_per_day == 0:
                self.current_day += 1

            self.cell_automaton.update(self.current_iteration, self.current_day)
            self.cell_automaton.draw(self.screen)

            self.update_statistics()

            self.repaint()

            if self.current_day >= self.config.max_days or (
                    self.auto_stop_enabled and self.cell_automaton.no_infected()):
                self.toggle_pause()
                self.simulation_data_saved.emit(self.config.max_days * self.config.iterations_per_day)
                self.auto_stop_triggered = True

                if (self.current_simulation + 1) < self.config.num_runs:
                    print(self.current_simulation, self.config.num_runs)
                    self.current_simulation += 1
                    self.start_simulation(self.config)



    def update_statistics(self):
        if self.cell_automaton:
            healthy, infected, latent, dead = self.cell_automaton.get_statistics()
            self.statistics_updated.emit(self.current_day, healthy, latent, infected, dead)

    def set_polygon(self, polygon_points, scale):
        self.polygon_points = polygon_points
        self.scale = scale

        if self.polygon_points:
            min_x = min(point[0] for point in self.polygon_points)
            max_x = max(point[0] for point in self.polygon_points)
            min_y = min(point[1] for point in self.polygon_points)
            max_y = max(point[1] for point in self.polygon_points)

            polygon_width = max_x - min_x
            polygon_height = max_y - min_y

            self.offset_x = (self.width() - polygon_width * self.scale) / 2 - min_x * self.scale
            self.offset_y = (self.height() - polygon_height * self.scale) / 2 - min_y * self.scale
        self.update_pygame_screen()
        self.update()

    def update_pygame_screen(self):
        self.screen.fill((0, 0, 0))
        if hasattr(self, 'polygon_points') and self.polygon_points:
            scaled_points = [
                (
                    (x * self.scale + self.offset_x),
                    (y * self.scale + self.offset_y)
                )
                for x, y in self.polygon_points
            ]
            pygame.draw.polygon(self.screen, (255, 255, 255), scaled_points, 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.screen:
            image = pygame.image.tostring(self.screen, 'RGB')
            qt_image = QImage(image, 600, 400, QImage.Format_RGB888)
            painter.drawImage(0, 0, qt_image)
