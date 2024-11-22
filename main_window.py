from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QSpacerItem, QSizePolicy, QScrollArea, QGroupBox, QFormLayout
from game_widget import GameWidget
from statistics_widget import StatisticsWidget
from config import Config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automaton - Infection Simulation")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        self.config = Config()

        main_widget = QWidget()
        main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()

        scroll_area = QScrollArea()
        param_panel = QWidget()
        param_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        param_layout = QVBoxLayout()

        # Group 1: Simulation Parameters
        simulation_params_group = QGroupBox("Simulation Parameters")
        simulation_params_layout = QFormLayout()
        self.cell_count_input = QLineEdit(str(self.config.cell_count))
        self.infected_count_input = QLineEdit(str(self.config.infected_count))
        self.latent_prob_input = QLineEdit(str(self.config.latent_prob))
        self.cycles_per_day_input = QLineEdit(str(self.config.iterations_per_day))
        simulation_params_layout.addRow(QLabel("Cell Count"), self.cell_count_input)
        simulation_params_layout.addRow(QLabel("Infected Count"), self.infected_count_input)
        simulation_params_layout.addRow(QLabel("Latent Percentage"), self.latent_prob_input)
        simulation_params_layout.addRow(QLabel("Cycles per Day"), self.cycles_per_day_input)
        simulation_params_group.setLayout(simulation_params_layout)
        param_layout.addWidget(simulation_params_group)

        # Group 2: Infection Parameters
        infection_params_group = QGroupBox("Infection Parameters")
        infection_params_layout = QFormLayout()
        self.infection_probability_input = QLineEdit(str(self.config.infection_probability))
        self.infection_period_input = QLineEdit(str(self.config.infection_period))
        self.latent_to_active_probability_input = QLineEdit(str(self.config.latent_to_active_prob))
        self.infection_probability_latent_input = QLineEdit(str(self.config.infection_prob_latent))
        self.infection_probability_active_input = QLineEdit(str(self.config.infection_prob_healthy))
        self.death_probability_input = QLineEdit(str(self.config.death_probability))
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
        self.cell_speed_input = QLineEdit(str(self.config.cell_speed))
        self.cell_size_input = QLineEdit(str(self.config.cell_size))
        self.infection_radius_input = QLineEdit(str(self.config.infection_radius))
        cell_params_layout.addRow(QLabel("Cell Speed"), self.cell_speed_input)
        cell_params_layout.addRow(QLabel("Cell Size"), self.cell_size_input)
        cell_params_layout.addRow(QLabel("Cell Infection Radius"), self.infection_radius_input)
        cell_params_group.setLayout(cell_params_layout)
        param_layout.addWidget(cell_params_group)

        # Group 4: Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QVBoxLayout()
        auto_stop_checkbox = QCheckBox("Stop when no infected")
        auto_stop_checkbox.setChecked(True)
        auto_stop_checkbox.stateChanged.connect(self.toggle_auto_stop)
        controls_layout.addWidget(auto_stop_checkbox)

        show_radii_checkbox = QCheckBox("Show Infection Radius")
        show_radii_checkbox.setChecked(True)
        self.radius_visibility = True
        show_radii_checkbox.stateChanged.connect(self.toggle_radius_visibility)
        show_radii_checkbox.stateChanged.connect(self.set_radius_visibility)
        controls_layout.addWidget(show_radii_checkbox)

        button_height = 35

        start_button = QPushButton("Start/Restart")
        start_button.setFixedHeight(button_height)
        start_button.clicked.connect(self.start_simulation)
        controls_layout.addWidget(start_button)

        pause_button = QPushButton("Pause/Resume")
        pause_button.setFixedHeight(button_height)
        pause_button.clicked.connect(self.pause_simulation)
        controls_layout.addWidget(pause_button)

        save_button = QPushButton("Save Plot")
        save_button.setFixedHeight(button_height)
        save_button.clicked.connect(self.save_plot)
        controls_layout.addWidget(save_button)

        toggle_button = QPushButton("Show/Hide Animation")
        toggle_button.setFixedHeight(button_height)
        toggle_button.clicked.connect(self.toggle_animation_visibility)
        controls_layout.addWidget(toggle_button)

        controls_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controls_group.setLayout(controls_layout)
        param_layout.addWidget(controls_group)

        param_panel.setLayout(param_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(param_panel)

        layout.addWidget(scroll_area, 0, 0, 2, 1)

        self.game_widget = GameWidget(self)
        layout.addWidget(self.game_widget, 0, 1)

        self.plot_widget = StatisticsWidget(self, config=self.config)
        scroll_area_plot = QScrollArea()
        scroll_area_plot.setWidgetResizable(True)
        scroll_area_plot.setWidget(self.plot_widget)
        layout.addWidget(scroll_area_plot, 1, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.game_widget.statistics_updated.connect(self.plot_widget.add_data)

    def start_simulation(self):
        self.config.cell_count = int(self.cell_count_input.text())
        self.config.infected_count = int(self.infected_count_input.text())
        self.config.latent_prob = float(self.latent_prob_input.text())
        self.config.iterations_per_day = int(self.cycles_per_day_input.text())
        self.config.infection_probability = float(self.infection_probability_input.text())
        self.config.infection_radius = int(self.infection_radius_input.text())
        self.config.infection_period = int(self.infection_period_input.text())
        self.config.latent_to_active_prob = float(self.latent_to_active_probability_input.text())
        self.config.infection_prob_latent = float(self.infection_probability_latent_input.text())
        self.config.infection_prob_active = float(self.infection_probability_active_input.text())
        self.config.cell_speed = float(self.cell_speed_input.text())
        self.config.death_probability = float(self.death_probability_input.text())
        self.config.cell_size = int(self.cell_size_input.text())

        self.game_widget.start_simulation(self.config)
        self.plot_widget.reset_data()
        self.set_radius_visibility()

    def pause_simulation(self):
        self.game_widget.toggle_pause()

    def toggle_auto_stop(self):
        self.game_widget.toggle_auto_stop()

    def save_plot(self):
        self.plot_widget.save_plot()

    def toggle_animation_visibility(self):
        self.game_widget.setVisible(not self.game_widget.isVisible())

    def toggle_radius_visibility(self):
        self.radius_visibility = not self.radius_visibility

    def set_radius_visibility(self):
        self.game_widget.set_radius_visible(self.radius_visibility)