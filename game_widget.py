import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QImage, QFont
from automaton import Automaton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)  # Розмір вікна симуляції

        # Ініціалізація Pygame
        pygame.init()
        self.screen = pygame.Surface((600, 400))  # Розмір симуляції
        self.automaton = None

        # Таймер для оновлення Pygame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(16)  # ~60 FPS

        # Ініціалізація графіка
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(600, 200)  # Розмір графіка
        self.canvas.setStyleSheet("background-color:transparent;")  # Прозорий фон
        self.canvas.setContentsMargins(0, 0, 0, 0)
        self.figure.patch.set_facecolor('none')
        self.ax.set_facecolor('#253D47')  # Темно-блакитний фон для графіка

        self.time_data = []
        self.healthy_data = []
        self.infected_data = []
        self.recovered_data = []
        self.time_step = 0

        # Текст для R всередині графіка
        self.r_label_in_graph = None

    def start_simulation(self, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period, infection_enabled=True, death_enabled=True):
        self.automaton = Automaton(600, 400, cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period, infection_enabled, death_enabled)
        self.time_data.clear()
        self.healthy_data.clear()
        self.infected_data.clear()
        self.recovered_data.clear()
        self.time_step = 0

    def game_loop(self):
        if self.automaton:
            self.automaton.update()
            self.automaton.draw(self.screen)
            self.repaint()

            # Оновлюємо статистику для графіка
            self.time_step += 1
            healthy, infected, recovered = self.automaton.get_statistics()
            self.time_data.append(self.time_step)
            self.healthy_data.append(healthy)
            self.infected_data.append(infected)
            self.recovered_data.append(recovered)
            self.update_plot()

    def paintEvent(self, event):
        # Рендеринг Pygame на PyQt5
        painter = QPainter(self)
        image = pygame.image.tostring(self.screen, 'RGB')
        qt_image = QImage(image, 600, 400, QImage.Format_RGB888)
        painter.drawImage(0, 0, qt_image)

    def update_plot(self):
        self.ax.clear()
        self.ax.set_facecolor('#253D47')  # Темний фон самого графіка

        # Налаштування кольорів областей
        self.ax.fill_between(self.time_data, 0, self.healthy_data, color='#7FB3D5', label='Susceptible')  # Темно-блакитний
        self.ax.fill_between(self.time_data, self.healthy_data, [h + i for h, i in zip(self.healthy_data, self.infected_data)], color='#F1948A', label='Infectious')  # Червоний
        self.ax.fill_between(self.time_data, [h + i for h, i in zip(self.healthy_data, self.infected_data)], [h + i + r for h, i, r in zip(self.healthy_data, self.infected_data, self.recovered_data)], color='#424949', label='Removed')  # Темно-сірий

        # Додаємо текст R всередині графіка
        if self.r_label_in_graph:
            self.r_label_in_graph.remove()
        self.r_label_in_graph = self.ax.text(0.9, 0.9, f"R ≈ {self.calculate_r_value():.2f}", transform=self.ax.transAxes, fontsize=12, color='white', ha='center')

        # Переміщуємо легенду вниз, щоб не перекривала R
        self.ax.legend(loc='lower left', facecolor='#253D47', edgecolor='white')

        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.canvas.draw()

    def calculate_r_value(self):
        # Формула для обчислення R
        if len(self.infected_data) > 1 and max(self.infected_data) > 0:
            r_value = (max(self.infected_data) - min(self.infected_data)) / max(self.infected_data)
            return max(1, r_value)  # Проста формула для демонстрації
        return 1.0

    def quit(self):
        pygame.quit()
