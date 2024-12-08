from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StatisticsWidget(QWidget):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(600, 350)
        self.canvas.setStyleSheet("background-color:white;")
        self.canvas.setContentsMargins(0, 0, 0, 0)
        self.figure.patch.set_facecolor('none')
        self.set_plot_background()

        self.time_data = []
        self.healthy_data = []
        self.latent_data = []
        self.infected_data = []
        self.dead_data = []

        self.healthy_label = QLabel("Healthy: 0")
        self.latent_label = QLabel("Latent: 0")
        self.infected_label = QLabel("Infected: 0")
        self.dead_label = QLabel("Dead: 0")

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.healthy_label)
        label_layout.addWidget(self.latent_label)
        label_layout.addWidget(self.infected_label)
        label_layout.addWidget(self.dead_label)

        layout = QVBoxLayout()
        layout.addLayout(label_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def set_plot_background(self):
        self.ax.set_facecolor('white')
        for spine in self.ax.spines.values():
            spine.set_color('black')
        self.ax.tick_params(axis='both', colors='black')
        self.ax.xaxis.label.set_color('black')
        self.ax.yaxis.label.set_color('black')

    def update_plot(self):
        self.ax.clear()
        self.set_plot_background()

        total_population = max((h + l + i + d for h, l, i, d in
                                zip(self.healthy_data, self.latent_data, self.infected_data, self.dead_data)),
                               default=0)
        if total_population == 0:
            total_population = len(self.healthy_data)

        latent_infected = [l + i for l, i in zip(self.latent_data, self.infected_data)]
        dead_latent_infected = [l + i + d for l, i, d in zip(self.latent_data, self.infected_data, self.dead_data)]

        self.ax.fill_between(self.time_data, 0, self.latent_data, color=[c/255 for c in self.config.color_latent],
                             label='Latent')
        self.ax.fill_between(self.time_data, self.latent_data, latent_infected, color=[c/255 for c in self.config.color_active],
                             label='Infectious')
        self.ax.fill_between(self.time_data, latent_infected, dead_latent_infected, color=[c/255 for c in self.config.color_dead], label='Dead')

        if total_population - max(dead_latent_infected, default=0) > 0:
            self.ax.fill_between(self.time_data, dead_latent_infected, [total_population] * len(dead_latent_infected),
                                 color=[c/255 for c in self.config.color_healthy], label='Susceptible')

        legend = self.ax.legend(loc='upper left', facecolor=(37 / 255, 61 / 255, 71 / 255), edgecolor=(1, 1, 1))
        for text in legend.get_texts():
            text.set_color((1, 1, 1))
        self.canvas.draw()

        self.update_labels()

    def update_labels(self):
        self.healthy_label.setText(f"Healthy: {self.healthy_data[-1] if self.healthy_data else 0}")
        self.latent_label.setText(f"Latent: {self.latent_data[-1] if self.latent_data else 0}")
        self.infected_label.setText(f"Infected: {self.infected_data[-1] if self.infected_data else 0}")
        self.dead_label.setText(f"Dead: {self.dead_data[-1] if self.dead_data else 0}")

    def save_plot(self):
        self.figure.savefig('simulation_plot.png', bbox_inches='tight', dpi=300)

    def add_data(self, day, healthy, latent, infected, dead):
        self.time_data.append(day)
        self.healthy_data.append(healthy)
        self.latent_data.append(latent)
        self.infected_data.append(infected)
        self.dead_data.append(dead)
        self.update_plot()

    def reset_data(self):
        self.time_data.clear()
        self.healthy_data.clear()
        self.latent_data.clear()
        self.infected_data.clear()
        self.dead_data.clear()
        self.update_plot()