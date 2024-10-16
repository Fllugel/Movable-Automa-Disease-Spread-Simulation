import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QImage
from automaton import Automaton, BACKGROUND_DARK, BACKGROUND_LIGHT
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)
        pygame.init()
        self.screen = pygame.Surface((600, 400))
        self.automaton = None
        self.theme = 'dark'  # Темна тема за замовчуванням
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)

        # Ініціалізація графіка
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
        self.time_step = 0

    def set_plot_background(self):
        if self.theme == 'dark':
            self.ax.set_facecolor('#253D47')
            self.ax.spines['bottom'].set_color('white')
            self.ax.spines['top'].set_color('white')
            self.ax.spines['left'].set_color('white')
            self.ax.spines['right'].set_color('white')
            self.ax.tick_params(axis='x', colors='white')
            self.ax.tick_params(axis='y', colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
        else:
            self.ax.set_facecolor('#FFFFFF')
            self.ax.spines['bottom'].set_color('black')
            self.ax.spines['top'].set_color('black')
            self.ax.spines['left'].set_color('black')
            self.ax.spines['right'].set_color('black')
            self.ax.tick_params(axis='x', colors='black')
            self.ax.tick_params(axis='y', colors='black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')

    def toggle_theme(self):
        self.theme = 'light' if self.theme == 'dark' else 'dark'
        self.set_plot_background()

    def start_simulation(self, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period):
        self.automaton = Automaton(600, 400, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period)
        self.time_data.clear()
        self.healthy_data.clear()
        self.infected_data.clear()
        self.recovered_data.clear()
        self.time_step = 0

    def game_loop(self):
        if self.automaton:
            self.automaton.update()
            background_color = BACKGROUND_DARK if self.theme == 'dark' else BACKGROUND_LIGHT
            self.automaton.draw(self.screen, background_color)
            self.repaint()
            self.update_statistics()

    def update_statistics(self):
        self.time_step += 1
        healthy, infected, recovered = self.automaton.get_statistics()
        self.time_data.append(self.time_step)
        self.healthy_data.append(healthy)
        self.infected_data.append(infected)
        self.recovered_data.append(recovered)
        self.update_plot()

    def paintEvent(self, event):
        painter = QPainter(self)
        image = pygame.image.tostring(self.screen, 'RGB')
        qt_image = QImage(image, 600, 400, QImage.Format_RGB888)
        painter.drawImage(0, 0, qt_image)

    def update_plot(self):
        self.ax.clear()
        self.set_plot_background()
        total_population = [h + i + r for h, i, r in zip(self.healthy_data, self.infected_data, self.recovered_data)]
        self.ax.fill_between(self.time_data, [i for i in self.infected_data], total_population, color='#7FB3D5', label='Susceptible')
        self.ax.fill_between(self.time_data, [i for i in self.infected_data], [i + r for i, r in zip(self.infected_data, self.recovered_data)], color='#424949', label='Recovered')
        self.ax.fill_between(self.time_data, 0, self.infected_data, color='#F1948A', label='Infectious')
        self.ax.legend(loc='lower left', facecolor='#253D47' if self.theme == 'dark' else '#FFFFFF', edgecolor='white')
        self.canvas.draw()

    def quit(self):
        pygame.quit()
