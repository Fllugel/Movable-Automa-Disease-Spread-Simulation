from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, \
    QSpacerItem, QSizePolicy, QScrollArea, QGroupBox, QFormLayout, QMessageBox, QComboBox
from game_widget import GameWidget
from statistics_widget import StatisticsWidget
from config import Config
from polygon import Polygon


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cellular Automaton - Infection Simulation")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1200, 800)

        self.config = Config()
        self.polygon = Polygon()

        main_widget = QWidget()
        main_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout()

        scroll_area = QScrollArea()
        param_panel = QWidget()
        param_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        param_layout = QVBoxLayout()

        # Group 1: Simulation Parameters
        simulation_params_group = QGroupBox("Simulation Parameters")
        simulation_params_layout = QFormLayout()
        self.cell_count_input = QLineEdit(str(self.config.cell_count))
        self.infected_count_input = QLineEdit(str(self.config.infected_count))
        self.latent_prob_input = QLineEdit(str(self.config.latent_prob))
        self.cycles_per_day_input = QLineEdit(str(self.config.iterations_per_day))
        self.infection_checks_per_iter_input = QLineEdit(str(self.config.infection_checks_per_iter))
        simulation_params_layout.addRow(QLabel("Cell Count"), self.cell_count_input)
        simulation_params_layout.addRow(QLabel("Infected Count"), self.infected_count_input)
        simulation_params_layout.addRow(QLabel("Latent Percentage"), self.latent_prob_input)
        simulation_params_layout.addRow(QLabel("Cycles per Day"), self.cycles_per_day_input)
        simulation_params_layout.addRow(QLabel("Checks Infection each (n) Iteration n ="),
                                        self.infection_checks_per_iter_input)
        simulation_params_group.setLayout(simulation_params_layout)
        param_layout.addWidget(simulation_params_group)

        # Group 2: Infection Parameters
        infection_params_group = QGroupBox("Infection Parameters")
        infection_params_layout = QFormLayout()
        self.latent_to_active_probability_input = QLineEdit(str(self.config.latent_to_active_prob))
        self.infection_probability_latent_input = QLineEdit(str(self.config.infection_prob_latent))
        self.infection_probability_healthy_input = QLineEdit(str(self.config.infection_prob_healthy))
        self.death_probability_input = QLineEdit(str(self.config.death_probability))
        infection_params_layout.addRow(QLabel("Latent to Active Probability"), self.latent_to_active_probability_input)
        infection_params_layout.addRow(QLabel("Infection Probability (Latent)"),
                                       self.infection_probability_latent_input)
        infection_params_layout.addRow(QLabel("Infection Probability (Healthy)"),
                                       self.infection_probability_healthy_input)
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

        show_radii_checkbox = QCheckBox("Show Infection Radius")
        show_radii_checkbox.setChecked(True)
        show_radii_checkbox.stateChanged.connect(self.toggle_radius_visibility)
        controls_layout.addWidget(show_radii_checkbox)

        show_hide_checkbox = QCheckBox("Show/Hide Animation")
        show_hide_checkbox.setChecked(True)
        show_hide_checkbox.stateChanged.connect(self.toggle_animation_visibility)
        controls_layout.addWidget(show_hide_checkbox)

        # Group 5: Polygon Type
        polygon_group = QGroupBox("Polygon Type")
        polygon_layout = QFormLayout()
        self.polygon_type_combo = QComboBox()
        self.polygon_type_combo.addItem("Trench")
        self.polygon_type_combo.addItem("Office")
        self.polygon_type_combo.addItem("Open Area")
        polygon_layout.addRow(QLabel("Select Polygon Type:"), self.polygon_type_combo)

        # self.polygon_type_combo.currentIndexChanged.connect(self.create_polygon)
        polygon_group.setLayout(polygon_layout)
        param_layout.addWidget(polygon_group)

        # Group 6: Multiple Runs
        multiple_runs_group = QGroupBox("Multiple Runs")
        multiple_runs_layout = QFormLayout()

        self.num_runs_input = QLineEdit(str(self.config.num_runs))
        self.max_days_input = QLineEdit(str(self.config.max_days))
        self.stop_on_no_infected_checkbox = QCheckBox("Stop when no infected")
        self.stop_on_no_infected_checkbox.setChecked(True)
        self.stop_on_no_infected_checkbox.stateChanged.connect(self.toggle_auto_stop)

        multiple_runs_layout.addRow(QLabel("Number of Runs"), self.num_runs_input)
        multiple_runs_layout.addRow(QLabel("Max Days per Run"), self.max_days_input)
        multiple_runs_layout.addRow(self.stop_on_no_infected_checkbox)

        multiple_runs_group.setLayout(multiple_runs_layout)
        param_layout.addWidget(multiple_runs_group)

        button_height = 35

        start_button = QPushButton("Start/Restart")
        start_button.setFixedHeight(button_height)
        start_button.clicked.connect(self.start_simulation)
        controls_layout.addWidget(start_button)

        pause_button = QPushButton("Pause/Resume")
        pause_button.setFixedHeight(button_height)
        pause_button.clicked.connect(self.pause_simulation)
        controls_layout.addWidget(pause_button)

        save_current_button = QPushButton("Save Current Data and Plot")
        save_current_button.setFixedHeight(button_height)
        save_current_button.clicked.connect(self.save_current_simulation_data_and_plot)
        controls_layout.addWidget(save_current_button)

        save_average_button = QPushButton("Save Average Data and Plot")
        save_average_button.setFixedHeight(button_height)
        save_average_button.clicked.connect(self.save_average_data_and_plot)
        controls_layout.addWidget(save_average_button)

        controls_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        controls_group.setLayout(controls_layout)
        param_layout.addWidget(controls_group)

        param_panel.setLayout(param_layout)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(param_panel)

        layout.addWidget(scroll_area, 0, 0, 2, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)

        self.game_widget = GameWidget(self)
        self.game_widget.setFixedWidth(600)
        layout.addWidget(self.game_widget, 0, 1)

        self.polygon_type_combo.setCurrentText("Open Area")
        self.create_polygon()

        self.plot_widget = StatisticsWidget(self, config=self.config)
        self.plot_widget.setFixedWidth(600)
        scroll_area_plot = QScrollArea()
        scroll_area_plot.setWidgetResizable(True)
        scroll_area_plot.setWidget(self.plot_widget)
        layout.addWidget(scroll_area_plot, 1, 1)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.game_widget.simulation_data_saved.connect(self.plot_widget.save_current_simulation_data)
        self.game_widget.statistics_updated.connect(self.plot_widget.add_data)

    def create_polygon(self):
        try:
            if self.polygon_type_combo.currentText() == "Trench":
                self.polygon.current_polygon, self.scale = Polygon.create_trench()
            elif self.polygon_type_combo.currentText() == "Office":
                self.polygon.current_polygon, self.scale = Polygon.create_office()
            elif self.polygon_type_combo.currentText() == "Open Area":
                self.polygon.current_polygon, self.scale = Polygon.create_open_area()
            else:
                raise ValueError("Unknown polygon type.")

            self.game_widget.set_polygon(self.polygon.current_polygon, self.scale)
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def start_simulation(self):
        try:
            self.create_polygon()
            if not self.polygon.current_polygon:
                raise ValueError("Polygon not selected. Please select a polygon for the simulation.")

            self.config.polygon_points = self.polygon.current_polygon
            self.config.cell_count = int(self.cell_count_input.text())
            self.config.infected_count = int(self.infected_count_input.text())
            self.config.latent_prob = float(self.latent_prob_input.text())
            self.config.iterations_per_day = int(self.cycles_per_day_input.text())
            self.config.infection_checks_per_iter = int(self.infection_checks_per_iter_input.text())
            self.config.infection_radius = int(self.infection_radius_input.text())
            self.config.latent_to_active_prob = float(self.latent_to_active_probability_input.text())
            self.config.infection_prob_latent = float(self.infection_probability_latent_input.text())
            self.config.infection_prob_healthy = float(self.infection_probability_healthy_input.text())
            self.config.cell_speed = float(self.cell_speed_input.text())
            self.config.death_probability = float(self.death_probability_input.text())
            self.config.cell_size = float(self.cell_size_input.text())
            self.config.num_runs = int(self.num_runs_input.text())
            self.config.max_days = int(self.max_days_input.text())

            self.game_widget.current_simulation = 0
            self.game_widget.start_simulation(self.config)
            self.plot_widget.reset_data()
            self.plot_widget.simulations_data = []
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def pause_simulation(self):
        self.game_widget.toggle_pause()

    def toggle_auto_stop(self):
        self.game_widget.toggle_auto_stop()

    def save_current_simulation_data_and_plot(self):
        self.plot_widget.save_current_simulation_data_and_plot()

    def save_average_data_and_plot(self):
        self.plot_widget.save_average_data_and_plot()

    def toggle_animation_visibility(self):
        self.game_widget.setVisible(not self.game_widget.isVisible())

    def toggle_radius_visibility(self):
        self.config.show_radius = not self.config.show_radius