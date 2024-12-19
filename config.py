class Config:
    def __init__(self, polygon_points=None, cell_count=1500, infected_count=1, latent_prob=0.25, iterations_per_day=3,
                 infection_probability=0.25, infection_radius=10, infection_period=225,
                 latent_to_active_prob=0, infection_prob_latent=0.14, infection_prob_healthy=0.1,
                 cell_speed=0.5, death_probability=0.104, cell_size=3, infection_checks_per_iter=20, show_radius=True,
                 color_healthy=(127, 179, 213), color_latent=(203, 157, 240),
                 color_active=(255, 100, 100), color_dead=(0, 0, 0),
                 background_color=(0, 0, 0)):
        if not polygon_points:
            polygon_points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        self.polygon_points = polygon_points
        self.show_radius = show_radius
        self.infection_checks_per_iter = infection_checks_per_iter
        self.cell_count = cell_count
        self.infected_count = infected_count
        self.latent_prob = latent_prob
        self.iterations_per_day = iterations_per_day
        # self.infection_probability = infection_probability
        self.infection_radius = infection_radius
        self.infection_period = infection_period
        self.latent_to_active_prob = latent_to_active_prob
        self.infection_prob_latent = infection_prob_latent
        self.infection_prob_healthy = infection_prob_healthy
        self.cell_speed = cell_speed
        self.death_probability = death_probability
        self.cell_size = cell_size
        self.color_healthy = color_healthy
        self.color_latent = color_latent
        self.color_active = color_active
        self.color_dead = color_dead
        self.background_color = background_color
