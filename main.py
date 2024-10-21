import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QSpacerItem,
                             QSizePolicy, QScrollArea, QLayout)
from game_widget import GameWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automaton - Infection Simulation")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        main_widget = QWidget()
        main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()
        layout.setSizeConstraint(QLayout.SetDefaultConstraint)

        scroll_area = QScrollArea()
        param_panel = QWidget()
        param_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        param_layout = QVBoxLayout()
        param_layout.setSpacing(3)

        self.cell_count_input = QLineEdit("500")
        self.infected_count_input = QLineEdit("10")
        self.cell_speed_input = QLineEdit("0.8")
        self.infection_probability_input = QLineEdit("0.5")
        self.infection_radius_input = QLineEdit("10")
        self.infection_period_input = QLineEdit("150")
        self.death_probability_input = QLineEdit("0.08")
        self.cell_size_input = QLineEdit("3")

        param_layout.addWidget(QLabel("Cell Count"))
        param_layout.addWidget(self.cell_count_input)
        param_layout.addWidget(QLabel("Infected Count"))
        param_layout.addWidget(self.infected_count_input)
        param_layout.addWidget(QLabel("Cell Speed"))
        param_layout.addWidget(self.cell_speed_input)
        param_layout.addWidget(QLabel("Infection Probability"))
        param_layout.addWidget(self.infection_probability_input)
        param_layout.addWidget(QLabel("Infection Radius"))
        param_layout.addWidget(self.infection_radius_input)
        param_layout.addWidget(QLabel("Infection Period"))
        param_layout.addWidget(self.infection_period_input)
        param_layout.addWidget(QLabel("Death Probability"))
        param_layout.addWidget(self.death_probability_input)
        param_layout.addWidget(QLabel("Cell Size"))

        param_layout.addWidget(self.cell_size_input)
        auto_stop_checkbox = QCheckBox("Stop when no infected")
        auto_stop_checkbox.setFixedHeight(20)
        auto_stop_checkbox.stateChanged.connect(self.toggle_auto_stop)
        param_layout.addWidget(auto_stop_checkbox)

        start_button = QPushButton("Start/Restart")
        start_button.setFixedHeight(30)
        start_button.clicked.connect(self.start_simulation)
        param_layout.addWidget(start_button)

        pause_button = QPushButton("Pause/Resume")
        pause_button.setFixedHeight(30)
        pause_button.clicked.connect(self.pause_simulation)
        param_layout.addWidget(pause_button)

        save_button = QPushButton("Save Plot")
        save_button.setFixedHeight(30)
        save_button.clicked.connect(self.save_plot)
        param_layout.addWidget(save_button)

        param_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        param_panel.setLayout(param_layout)

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(param_panel)

        layout.addWidget(scroll_area, 0, 0, 2, 1)

        self.game_widget = GameWidget(self)
        layout.addWidget(self.game_widget, 0, 1)
        layout.addWidget(self.game_widget.canvas, 1, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def start_simulation(self):
        cell_count = int(self.cell_count_input.text())
        infected_count = int(self.infected_count_input.text())
        cell_speed = float(self.cell_speed_input.text())
        infection_probability = float(self.infection_probability_input.text())
        infection_radius = int(self.infection_radius_input.text())
        infection_period = int(self.infection_period_input.text())
        death_probability = float(self.death_probability_input.text())
        cell_size = int(self.cell_size_input.text())

        self.game_widget.start_simulation(cell_count, infected_count, cell_speed, infection_probability,
                                          infection_radius, infection_period, death_probability, cell_size)

    def pause_simulation(self):
        self.game_widget.toggle_pause()

    def toggle_auto_stop(self):
        self.game_widget.toggle_auto_stop()

    def save_plot(self):
        self.game_widget.save_plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())