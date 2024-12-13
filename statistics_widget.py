from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QInputDialog
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class StatisticsWidget(QWidget):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.config = config
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 7))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(600, 500)
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
        for ax in [self.ax1, self.ax2]:
            ax.set_facecolor('white')
            for spine in ax.spines.values():
                spine.set_color('black')
            ax.tick_params(axis='both', colors='black')
            ax.xaxis.label.set_color('black')
            ax.yaxis.label.set_color('black')

    def update_plot(self):
        # Update the first plot (the classic stacked plot)
        self.ax1.clear()
        self.set_plot_background()

        total_population = max((h + l + i + d for h, l, i, d in
                                zip(self.healthy_data, self.latent_data, self.infected_data, self.dead_data)),
                               default=0)
        if total_population == 0:
            total_population = len(self.healthy_data)

        latent_infected = [l + i for l, i in zip(self.latent_data, self.infected_data)]
        dead_latent_infected = [l + i + d for l, i, d in zip(self.latent_data, self.infected_data, self.dead_data)]

        self.ax1.fill_between(self.time_data, 0, self.latent_data, color=[c/255 for c in self.config.color_latent],
                             label='Latent')
        self.ax1.fill_between(self.time_data, self.latent_data, latent_infected, color=[c/255 for c in self.config.color_active],
                             label='Infectious')
        self.ax1.fill_between(self.time_data, latent_infected, dead_latent_infected, color=[c/255 for c in self.config.color_dead], label='Dead')

        if total_population - max(dead_latent_infected, default=0) > 0:
            self.ax1.fill_between(self.time_data, dead_latent_infected, [total_population] * len(dead_latent_infected),
                                 color=[c/255 for c in self.config.color_healthy], label='Susceptible')

        self.ax1.legend(loc='upper left', facecolor=(37 / 255, 61 / 255, 71 / 255), edgecolor=(1, 1, 1))

        # Update the second plot (two independent lines: one for latent and one for active)
        self.ax2.clear()
        self.set_plot_background()

        # Plot the latent population (blue color)
        self.ax2.plot(self.time_data, self.latent_data, label='Latent', color=[c/255 for c in self.config.color_latent], linestyle='-', linewidth=2)

        # Plot the active population (red color, only infected)
        self.ax2.plot(self.time_data, self.infected_data, label='Active (Infected)', color=[c/255 for c in self.config.color_active], linestyle='-', linewidth=2)

        self.ax2.set_ylabel('Population')
        self.ax2.set_xlabel('Time')
        self.ax2.legend(loc='upper left', facecolor=(37 / 255, 61 / 255, 71 / 255), edgecolor=(1, 1, 1))

        self.canvas.draw()

        self.update_labels()

    def update_labels(self):
        self.healthy_label.setText(f"Healthy: {self.healthy_data[-1] if self.healthy_data else 0}")
        self.latent_label.setText(f"Latent: {self.latent_data[-1] if self.latent_data else 0}")
        self.infected_label.setText(f"Infected: {self.infected_data[-1] if self.infected_data else 0}")
        self.dead_label.setText(f"Dead: {self.dead_data[-1] if self.dead_data else 0}")

    def save_data_and_plot(self):
        if not self.time_data:
            print("No data to save.")
            return

        unique_days = set()
        filtered_data = {"Day": [], "Healthy": [], "Latent": [], "Infected": [], "Dead": []}

        for i, day in enumerate(self.time_data):
            if day not in unique_days:
                unique_days.add(day)
                filtered_data["Day"].append(self.time_data[i])
                filtered_data["Healthy"].append(self.healthy_data[i])
                filtered_data["Latent"].append(self.latent_data[i])
                filtered_data["Infected"].append(self.infected_data[i])
                filtered_data["Dead"].append(self.dead_data[i])

        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Select folder to save", options=options)
        if not folder:
            return

        folder_name, ok = QInputDialog.getText(self, "Enter folder name", "Folder name:")
        if not ok or not folder_name:
            print("Folder name was not entered.")
            return

        full_folder_path = os.path.join(folder, folder_name)
        try:
            os.makedirs(full_folder_path, exist_ok=True)
        except Exception as e:
            print(f"Error creating folder: {e}")
            return

        df = pd.DataFrame(filtered_data)
        excel_path = os.path.join(full_folder_path, f"{folder_name}_data.xlsx")
        try:
            df.to_excel(excel_path, index=False)
            print(f"Data successfully saved to file {excel_path}.")
        except Exception as e:
            print(f"Error saving data: {e}")

        plot_path_ax1 = os.path.join(full_folder_path, f"{folder_name}_plot.png")
        try:
            fig1 = self.ax1.figure
            fig1.savefig(plot_path_ax1, bbox_inches='tight', dpi=300)
            print(f"Plots successfully saved to {plot_path_ax1}.")
        except Exception as e:
            print(f"Error saving plots: {e}")

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
