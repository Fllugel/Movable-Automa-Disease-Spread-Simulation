import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QImage
from automaton import Automaton, BACKGROUND_DARK
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)
        pygame.init()
        self.screen = pygame.Surface((600, 400))
        self.automaton = None
        self.is_paused = False
        self.auto_stop_enabled = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

        # Daily statistics labels
        self.daily_stats_label = QLabel("Day: 1\nDaily Counts:\nInfected: 0\nRecovered: 0\nDead: 0", self)
        self.daily_stats_label.move(620, 0)  # Positioning on the right side of the screen

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(600, 200)
        self.canvas.setStyleSheet("background-color:transparent;")
        self.canvas.setContentsMargins(0, 0, 0, 0)
        self.figure.patch.set_facecolor('none')
        self.set_plot_background()

        self.time_data = []
        self.healthy_data = []
        self.infected_data = []
        self.recovered_data = []
        self.dead_data = []
        self.time_step = 0
        self.cycles_per_day = 200  # Number of cycles representing a day
        self.cycle_counter = 0  # To keep track of cycles within a day
        self.current_day = 1  # Initialize the day counter

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
        self.automaton.running = not self.is_paused

    def toggle_auto_stop(self):
        self.auto_stop_enabled = not self.auto_stop_enabled

    def start_simulation(self, cell_count, infected_count, cell_speed, infection_probability, infection_radius,
                         infection_period, death_probability, cell_size):
        self.automaton = Automaton(600, 400, cell_count, infected_count, cell_speed, infection_probability,
                                   infection_radius, infection_period, death_probability, cell_size)
        self.time_data.clear()
        self.healthy_data.clear()
        self.infected_data.clear()
        self.recovered_data.clear()
        self.dead_data.clear()
        self.time_step = 0
        self.cycle_counter = 0  # Reset cycle counter
        self.current_day = 1  # Reset the day counter

    def game_loop(self):
        if self.automaton and not self.is_paused:
            self.automaton.update()
            self.automaton.draw(self.screen, BACKGROUND_DARK)
            self.repaint()
            self.update_statistics()
            if self.auto_stop_enabled:
                self.automaton.stop_if_no_infected()

    def update_statistics(self):
        # Отримуємо поточну кількість для кожного стану
        healthy, infected, recovered, dead = self.automaton.get_statistics()
        infected_count = infected
        recovered_count = recovered
        dead_count = dead

        # Оновлюємо текст у мітці для відображення цих значень
        self.daily_stats_label.setText(
            f"Infected: {infected_count}\nRecovered: {recovered_count}\nDead: {dead_count}"
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        image = pygame.image.tostring(self.screen, 'RGB')
        qt_image = QImage(image, 600, 400, QImage.Format_RGB888)
        painter.drawImage(0, 0, qt_image)

    def update_plot(self):
        self.ax.clear()
        self.set_plot_background()

        total_population = max([h + i + r + d for h, i, r, d in
                                zip(self.healthy_data, self.infected_data, self.recovered_data, self.dead_data)],
                               default=0)
        if total_population == 0:
            total_population = len(self.healthy_data)

        dead_recovered_infected = [i + r + d for i, r, d in
                                   zip(self.infected_data, self.recovered_data, self.dead_data)]
        recovered_infected = [i + r for i, r in zip(self.infected_data, self.recovered_data)]

        self.ax.fill_between(self.time_data, 0, self.infected_data, color='#F1948A', label='Infectious')
        self.ax.fill_between(self.time_data, self.infected_data, recovered_infected, color='#424949', label='Recovered')
        self.ax.fill_between(self.time_data, recovered_infected, dead_recovered_infected, color='black', label='Dead')

        if total_population - max(dead_recovered_infected) > 0:
            self.ax.fill_between(self.time_data, dead_recovered_infected,
                                 [total_population] * len(dead_recovered_infected), color='#7FB3D5',
                                 label='Susceptible')

        legend = self.ax.legend(loc='upper left', facecolor='#253D47', edgecolor='white')
        for text in legend.get_texts():
            text.set_color('white')
        self.canvas.draw()

    def save_plot(self):
        self.figure.savefig('simulation_plot.png', bbox_inches='tight', dpi=300)

    def quit(self):
        pygame.quit()
