from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLineEdit, QLabel, QPushButton, QCheckBox, QSpacerItem, QSizePolicy, QScrollArea, QGroupBox, QFormLayout, QMessageBox
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

        # Group 0: Polygon Parameters
        polygon_group = QGroupBox("Polygon Parameters")
        polygon_layout = QFormLayout()
        self.polygon_points_input = QLineEdit("[(0, 0), (100, 0), (100, 100), (0, 100)]")
        polygon_layout.addRow(QLabel("Polygon Bounds (list of tuples for x and y):"), self.polygon_points_input)
        create_polygon_button = QPushButton("Create Polygon")
        create_polygon_button.setFixedHeight(30)
        create_polygon_button.clicked.connect(self.generate_polygon)
        polygon_layout.addRow(create_polygon_button)
        polygon_group.setLayout(polygon_layout)
        param_layout.addWidget(polygon_group)

        # Group 1: Simulation Parameters
        simulation_params_group = QGroupBox("Simulation Parameters")
        simulation_params_layout = QFormLayout()
        self.cell_count_input = QLineEdit(str(self.config.cell_count))
        self.infected_count_input = QLineEdit(str(self.config.infected_count))
        self.latent_prob_input = QLineEdit(str(self.config.latent_prob))
        self.cycles_per_day_input = QLineEdit(str(self.config.iterations_per_day))
        self.infection_checks_per_iter_input = QLineEdit(str(self.config.infection_checks_per_iter))  # New location
        simulation_params_layout.addRow(QLabel("Cell Count"), self.cell_count_input)
        simulation_params_layout.addRow(QLabel("Infected Count"), self.infected_count_input)
        simulation_params_layout.addRow(QLabel("Latent Percentage"), self.latent_prob_input)
        simulation_params_layout.addRow(QLabel("Cycles per Day"), self.cycles_per_day_input)
        simulation_params_layout.addRow(QLabel("Checks Infection each (n) Iteration n ="), self.infection_checks_per_iter_input)  # New location
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

        show_hide_checkbox = QCheckBox("Show/Hide Animation")
        show_hide_checkbox.setChecked(True)
        show_hide_checkbox.stateChanged.connect(self.toggle_animation_visibility)
        controls_layout.addWidget(show_hide_checkbox)

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

    def generate_polygon(self):
        try:
            polygon_input = self.polygon_points_input.text().strip()
            polygon_input = polygon_input.replace(" ", "")
            if polygon_input.startswith("[") and polygon_input.endswith("]"):
                polygon_input = polygon_input[2:-2]
                self.current_polygon = [tuple(map(float, point.split(","))) for point in polygon_input.split("),(")]
                if len(self.current_polygon) < 3:
                    raise ValueError("Polygon must have at least 3 sides.")

                self.game_widget.set_polygon(self.current_polygon)
            else:
                raise ValueError("Invalid input format.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create polygon: {e}")

    def start_simulation(self):
        try:
            if not hasattr(self, "current_polygon") or not self.current_polygon:
                raise ValueError("Polygon is not generated. Please generate a polygon before starting the simulation.")

            self.config.polygon_points = self.current_polygon
            self.config.cell_count = int(self.cell_count_input.text())
            self.config.infected_count = int(self.infected_count_input.text())
            self.config.latent_prob = float(self.latent_prob_input.text())
            self.config.iterations_per_day = int(self.cycles_per_day_input.text())
            self.config.infection_checks_per_iter = int(
                self.infection_checks_per_iter_input.text())  # Read from new location
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
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

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