import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QCheckBox
from game_widget import GameWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automaton - Infection Simulation")
        self.setGeometry(100, 100, 1000, 700)

        main_widget = QWidget()
        layout = QVBoxLayout()

        top_layout = QHBoxLayout()

        param_panel = QWidget()
        param_layout = QVBoxLayout()

        self.cell_count_input = QLineEdit("500")
        self.infected_count_input = QLineEdit("10")
        self.cell_speed_input = QLineEdit("0.5")
        self.infection_probability_input = QLineEdit("0.05")
        self.infection_radius_input = QLineEdit("10")
        self.infection_period_input = QLineEdit("150")

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

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start_simulation)
        param_layout.addWidget(start_button)

        theme_toggle = QCheckBox("Toggle Theme")
        theme_toggle.stateChanged.connect(self.toggle_theme)
        param_layout.addWidget(theme_toggle)

        param_panel.setLayout(param_layout)
        top_layout.addWidget(param_panel)

        self.game_widget = GameWidget(self)
        top_layout.addWidget(self.game_widget)
        layout.addLayout(top_layout)

        layout.addWidget(self.game_widget.canvas)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def start_simulation(self):
        cell_count = int(self.cell_count_input.text())
        infected_count = int(self.infected_count_input.text())
        cell_speed = float(self.cell_speed_input.text())
        infection_probability = float(self.infection_probability_input.text())
        infection_radius = int(self.infection_radius_input.text())
        infection_period = int(self.infection_period_input.text())

        self.game_widget.start_simulation(cell_count, infected_count, cell_speed, infection_probability, infection_radius, infection_period)

    def toggle_theme(self):
        self.game_widget.toggle_theme()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
