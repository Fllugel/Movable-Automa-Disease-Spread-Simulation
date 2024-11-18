from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QSpacerItem,
                             QSizePolicy, QScrollArea, QLayout, QGroupBox, QFormLayout)
from game_widget import GameWidget

# Default values as constants
DEFAULT_CELL_COUNT = 500
DEFAULT_INFECTED_COUNT = 1
DEFAULT_LATENT_PROB = 0.25
DEFAULT_CYCLES_PER_DAY = 10
DEFAULT_INFECTION_PROBABILITY = 0.25
DEFAULT_INFECTION_RADIUS = 10
DEFAULT_INFECTION_PERIOD = 30
DEFAULT_LATENT_TO_ACTIVE_PROBABILITY = 0
DEFAULT_INFECTION_PROBABILITY_LATENT = 0.05
DEFAULT_INFECTION_PROBABILITY_ACTIVE = 0.1
DEFAULT_CELL_SPEED = 0.5
DEFAULT_DEATH_PROBABILITY = 0
DEFAULT_CELL_SIZE = 3

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

        # Group 1: Simulation Parameters
        simulation_params_group = QGroupBox("Simulation Parameters")
        simulation_params_layout = QFormLayout()
        self.cell_count_input = QLineEdit(str(DEFAULT_CELL_COUNT))
        self.infected_count_input = QLineEdit(str(DEFAULT_INFECTED_COUNT))
        self.latent_prob_input = QLineEdit(str(DEFAULT_LATENT_PROB))
        self.cycles_per_day_input = QLineEdit(str(DEFAULT_CYCLES_PER_DAY))
        simulation_params_layout.addRow(QLabel("Cell Count"), self.cell_count_input)
        simulation_params_layout.addRow(QLabel("Infected Count"), self.infected_count_input)
        simulation_params_layout.addRow(QLabel("Latent Percentage"), self.latent_prob_input)
        simulation_params_layout.addRow(QLabel("Cycles per Day"), self.cycles_per_day_input)
        simulation_params_group.setLayout(simulation_params_layout)
        param_layout.addWidget(simulation_params_group)

        # Group 2: Infection Parameters
        infection_params_group = QGroupBox("Infection Parameters")
        infection_params_layout = QFormLayout()
        self.infection_probability_input = QLineEdit(str(DEFAULT_INFECTION_PROBABILITY))
        self.infection_period_input = QLineEdit(str(DEFAULT_INFECTION_PERIOD))
        self.latent_to_active_probability_input = QLineEdit(str(DEFAULT_LATENT_TO_ACTIVE_PROBABILITY))
        self.infection_probability_latent_input = QLineEdit(str(DEFAULT_INFECTION_PROBABILITY_LATENT))
        self.infection_probability_active_input = QLineEdit(str(DEFAULT_INFECTION_PROBABILITY_ACTIVE))
        self.death_probability_input = QLineEdit(str(DEFAULT_DEATH_PROBABILITY))
        infection_params_layout.addRow(QLabel("Infection Probability"), self.infection_probability_input)
        infection_params_layout.addRow(QLabel("Infection Period"), self.infection_period_input)
        infection_params_layout.addRow(QLabel("Latent to Active Probability"), self.latent_to_active_probability_input)
        infection_params_layout.addRow(QLabel("Infection Probability (Latent)"), self.infection_probability_latent_input)
        infection_params_layout.addRow(QLabel("Infection Probability (Active)"), self.infection_probability_active_input)
        infection_params_layout.addRow(QLabel("Death Probability"), self.death_probability_input)
        infection_params_group.setLayout(infection_params_layout)
        param_layout.addWidget(infection_params_group)

        # Group 3: Cell Parameters
        cell_params_group = QGroupBox("Cell Parameters")
        cell_params_layout = QFormLayout()
        self.cell_speed_input = QLineEdit(str(DEFAULT_CELL_SPEED))
        self.cell_size_input = QLineEdit(str(DEFAULT_CELL_SIZE))
        self.infection_radius_input = QLineEdit(str(DEFAULT_INFECTION_RADIUS))
        cell_params_layout.addRow(QLabel("Cell Speed"), self.cell_speed_input)
        cell_params_layout.addRow(QLabel("Cell Size"), self.cell_size_input)
        cell_params_layout.addRow(QLabel("Cell Infection Radius"), self.infection_radius_input)
        cell_params_group.setLayout(cell_params_layout)
        param_layout.addWidget(cell_params_group)

        # Group 4: Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        auto_stop_checkbox = QCheckBox("Stop when no infected")
        auto_stop_checkbox.setFixedHeight(20)
        auto_stop_checkbox.setChecked(True)
        auto_stop_checkbox.stateChanged.connect(self.toggle_auto_stop)
        controls_layout.addWidget(auto_stop_checkbox)

        show_radii_checkbox = QCheckBox("Show Infection Radius")
        show_radii_checkbox.setFixedHeight(20)
        show_radii_checkbox.setChecked(True)
        self.radius_visibility = True
        show_radii_checkbox.stateChanged.connect(self.toggle_radius_visibility)
        show_radii_checkbox.stateChanged.connect(self.set_radius_visibility)
        controls_layout.addWidget(show_radii_checkbox)

        start_button = QPushButton("Start/Restart")
        start_button.setFixedHeight(30)
        start_button.clicked.connect(self.start_simulation)
        controls_layout.addWidget(start_button)

        pause_button = QPushButton("Pause/Resume")
        pause_button.setFixedHeight(30)
        pause_button.clicked.connect(self.pause_simulation)
        controls_layout.addWidget(pause_button)

        save_button = QPushButton("Save Plot")
        save_button.setFixedHeight(30)
        save_button.clicked.connect(self.save_plot)
        controls_layout.addWidget(save_button)

        toggle_button = QPushButton("Show/Hide Animation")
        toggle_button.setFixedHeight(30)
        toggle_button.clicked.connect(self.toggle_animation_visibility)
        controls_layout.addWidget(toggle_button)

        self.daily_stats_label = QLabel("Day 0\nInfected: 0\nLatent: 0\nDead: 0")
        controls_layout.addWidget(self.daily_stats_label)

        controls_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controls_group.setLayout(controls_layout)
        param_layout.addWidget(controls_group)

        param_panel.setLayout(param_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(param_panel)

        layout.addWidget(scroll_area, 0, 0, 2, 1)

        self.game_widget = GameWidget(self)
        self.game_widget.setVisible(True)
        self.game_widget.daily_stats_label = self.daily_stats_label
        layout.addWidget(self.game_widget, 0, 1)
        layout.addWidget(self.game_widget.canvas, 1, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def start_simulation(self):
        cell_count = int(self.cell_count_input.text())
        infected_count = int(self.infected_count_input.text())
        latent_count = float(self.latent_prob_input.text())
        cell_speed = float(self.cell_speed_input.text())
        infection_probability = float(self.infection_probability_input.text())
        infection_radius = int(self.infection_radius_input.text())
        infection_period_days = int(self.infection_period_input.text())
        death_probability = float(self.death_probability_input.text())
        cell_size = int(self.cell_size_input.text())
        cycles_per_day = int(self.cycles_per_day_input.text())

        latent_to_active_prob = float(self.latent_to_active_probability_input.text())
        infection_prob_latent = float(self.infection_probability_latent_input.text())
        infection_prob_active = float(self.infection_probability_active_input.text())

        self.game_widget.start_simulation(cell_count, infected_count, latent_count, cell_speed, infection_probability,
                                          infection_radius, infection_period_days, death_probability, cell_size,
                                          cycles_per_day, latent_to_active_prob, infection_prob_latent, infection_prob_active)

        self.set_radius_visibility()

    def pause_simulation(self):
        self.game_widget.toggle_pause()

    def toggle_auto_stop(self):
        self.game_widget.toggle_auto_stop()

    def save_plot(self):
        self.game_widget.save_plot()

    def toggle_animation_visibility(self):
        self.game_widget.setVisible(not self.game_widget.isVisible())

    def toggle_radius_visibility(self):
        self.radius_visibility = not self.radius_visibility

    def set_radius_visibility(self):
        self.game_widget.set_radius(self.radius_visibility)
