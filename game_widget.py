import pygame
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QImage
from cell_automaton import CellAutomaton
from config import Config

class GameWidget(QWidget):
    statistics_updated = pyqtSignal(int, int, int, int, int)

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

    def _initialize_pygame(self):
        pygame.init()
        self.screen = pygame.Surface((600, 400))

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def toggle_auto_stop(self):
        self.auto_stop_enabled = not self.auto_stop_enabled

    def set_radius_visible(self, show_radius):
        if self.cell_automaton:
            self.cell_automaton.show_radius = show_radius

    def start_simulation(self, config: Config):
        self.cell_automaton = CellAutomaton(config)
        self.current_day = 0
        self.config = config

    def game_loop(self):
        if self.cell_automaton and not self.is_paused:
            self.current_iteration += 1

            # Update the current day based on iterations_per_day
            if self.current_iteration % self.config.iterations_per_day == 0:
                self.current_day += 1

            self.cell_automaton.update(self.current_iteration, self.current_day)
            self.cell_automaton.draw(self.screen)

            self.update_statistics()

            self.repaint()

            if self.auto_stop_enabled and not self.auto_stop_triggered:
                if self.cell_automaton.no_infected():
                    self.toggle_pause()
                    self.auto_stop_triggered = True

    def update_statistics(self):
        if self.cell_automaton:
            healthy, infected, latent, dead = self.cell_automaton.get_statistics()
            self.statistics_updated.emit(self.current_day, healthy, latent, infected, dead)

    def paintEvent(self, event):
        painter = QPainter(self)
        image = pygame.image.tostring(self.screen, 'RGB')
        qt_image = QImage(image, 600, 400, QImage.Format_RGB888)
        painter.drawImage(0, 0, qt_image)