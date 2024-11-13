import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QSpacerItem,
                             QSizePolicy, QScrollArea, QLayout)
from PyQt5.QtGui import QPalette, QColor
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
        self.cell_speed_input = QLineEdit("0.5")
        self.infection_probability_input = QLineEdit("0.25")
        self.infection_radius_input = QLineEdit("10")
        self.infection_period_input = QLineEdit("30")
        self.death_probability_input = QLineEdit("0")
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

        self.cycles_per_day_input = QLineEdit("10")  # Default value for cycles per day
        param_layout.addWidget(QLabel("Cycles per Day"))
        param_layout.addWidget(self.cycles_per_day_input)

        auto_stop_checkbox = QCheckBox("Stop when no infected")
        auto_stop_checkbox.setFixedHeight(20)
        auto_stop_checkbox.stateChanged.connect(self.toggle_auto_stop)
        auto_stop_checkbox.setChecked(True)
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

        # Toggle Animation Visibility Button
        toggle_button = QPushButton("Show/Hide Animation")
        toggle_button.setFixedHeight(30)
        toggle_button.clicked.connect(self.toggle_animation_visibility)
        param_layout.addWidget(toggle_button)
        param_layout.addWidget(save_button)

        # Daily statistics label
        self.daily_stats_label = QLabel("Infected: 0\nRecovered: 0\nDead: 0")
        param_layout.addWidget(self.daily_stats_label)

        param_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        param_panel.setLayout(param_layout)

        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(param_panel)

        layout.addWidget(scroll_area, 0, 0, 2, 1)

        self.game_widget = GameWidget(self)
        self.game_widget.setVisible(True)  # Initialize as visible
        self.game_widget.daily_stats_label = self.daily_stats_label  # Reference to update daily stats
        layout.addWidget(self.game_widget, 0, 1)
        layout.addWidget(self.game_widget.canvas, 1, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    # main.py

    def start_simulation(self):
        cell_count = int(self.cell_count_input.text())
        infected_count = int(self.infected_count_input.text())
        cell_speed = float(self.cell_speed_input.text())
        infection_probability = float(self.infection_probability_input.text())
        infection_radius = int(self.infection_radius_input.text())
        infection_period_days = int(self.infection_period_input.text())
        death_probability = float(self.death_probability_input.text())
        cell_size = int(self.cell_size_input.text())
        cycles_per_day = int(self.cycles_per_day_input.text())

        infection_period_cycles = infection_period_days * cycles_per_day  # Convert days to cycles

        self.game_widget.start_simulation(cell_count, infected_count, cell_speed, infection_probability,
                                          infection_radius, infection_period_cycles, death_probability, cell_size,
                                          cycles_per_day)

    def pause_simulation(self):
        self.game_widget.toggle_pause()

    def toggle_auto_stop(self):
        self.game_widget.toggle_auto_stop()

    def save_plot(self):
        self.game_widget.save_plot()

    def toggle_animation_visibility(self):
        self.game_widget.setVisible(not self.game_widget.isVisible())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(255, 255, 255))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(0, 0, 255))
    palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
