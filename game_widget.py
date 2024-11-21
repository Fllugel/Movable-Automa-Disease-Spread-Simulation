import pygame
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from automaton import Automaton
from config import Config

class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = None
        self.setFixedSize(600, 400)
        pygame.init()
        self.screen = pygame.Surface((600, 400))
        self.automaton = None
        self.is_paused = False
        self.auto_stop_enabled = True
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

        # Daily statistics labels
        self.stats_label = QLabel("Day: 0\nInfected: 0\nLatent: 0\nDead: 0", self)
        self.stats_label.move(620, 0)  # Positioning on the right side of the screen

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(600, 200)
        self.canvas.setStyleSheet("background-color:transparent;")
        self.canvas.setContentsMargins(0, 0, 0, 0)
        self.figure.patch.set_facecolor('none')
        self.set_plot_background()

        self.time_data = []
        self.healthy_data = []
        self.latent_data = []
        self.infected_data = []
        self.dead_data = []
        self.time_step = 0
        self.cycles_per_day = 200
        self.cycle_counter = 0
        self.current_day = 1

    def set_plot_background(self):
        self.ax.set_facecolor('white')
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color('black')
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color('black')
        self.ax.tick_params(axis='x', colors='black')
        self.ax.tick_params(axis='y', colors='black')
        self.ax.xaxis.label.set_color('black')
        self.ax.yaxis.label.set_color('black')

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def toggle_auto_stop(self):
        self.auto_stop_enabled = not self.auto_stop_enabled

    def set_radius(self, show_radius):
        self.automaton.show_radius = show_radius

    def start_simulation(self, config: Config):
        self.automaton = Automaton(config)
        self.time_data.clear()
        self.healthy_data.clear()
        self.latent_data.clear()
        self.infected_data.clear()
        self.dead_data.clear()
        self.time_step = 0
        self.cycle_counter = 0
        self.current_day = 1
        self.cycles_per_day = config.cycles_per_day
        self.config = config

    def game_loop(self):
        if self.automaton:
            if not self.is_paused:
                self.automaton.update()
                self.cycle_counter += 1
                self.current_day = self.cycle_counter / self.cycles_per_day
                if self.automaton.running:
                    self.automaton.update_current_day(self.current_day)
                    self.update_statistics()
            self.automaton.draw(self.screen, self.config.background_color)
            self.repaint()
            if self.auto_stop_enabled:
                self.automaton.stop_if_no_infected()

    def update_statistics(self):
        healthy, infected, latent, dead = self.automaton.get_statistics()
        self.time_data.append(self.current_day)
        self.healthy_data.append(healthy)
        self.latent_data.append(latent)
        self.infected_data.append(infected)
        self.dead_data.append(dead)

        self.daily_stats_label.setText(
            f"Day: {self.current_day}\nInfected: {infected}\nLatent: {latent}\nDead: {dead}"
        )

        self.update_plot()

    def paintEvent(self, event):
        painter = QPainter(self)
        image = pygame.image.tostring(self.screen, 'RGB')
        qt_image = QImage(image, 600, 400, QImage.Format_RGB888)
        painter.drawImage(0, 0, qt_image)

    def update_plot(self):
        self.ax.clear()
        self.set_plot_background()

        total_population = max([h + l + i + d for h, l, i, d in
                                zip(self.healthy_data, self.latent_data, self.infected_data, self.dead_data)],
                               default=0)
        if total_population == 0:
            total_population = len(self.healthy_data)

        latent_infected = [l + i for l, i in zip(self.latent_data, self.infected_data)]
        dead_latent_infected = [l + i + d for l, i, d in zip(self.latent_data, self.infected_data, self.dead_data)]

        self.ax.fill_between(self.time_data, 0, self.latent_data, color='#F0C0F0', label='Latent')
        self.ax.fill_between(self.time_data, self.latent_data, latent_infected, color='#F1948A', label='Infectious')
        self.ax.fill_between(self.time_data, dead_latent_infected, [total_population] * len(dead_latent_infected), color='black', label='Dead')

        if total_population - max(dead_latent_infected) > 0:
            self.ax.fill_between(self.time_data, dead_latent_infected,
                                 [total_population] * len(dead_latent_infected), color='#7FB3D5',
                                 label='Susceptible')

        legend = self.ax.legend(loc='upper left', facecolor='#253D47', edgecolor='white')
        for text in legend.get_texts():
            text.set_color('white')
        self.canvas.draw()

    def save_plot(self):
        self.figure.savefig('simulation_plot.png', bbox_inches='tight', dpi=300)

    def quit(self):
        pygame.quit()