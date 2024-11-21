class Config:
    def __init__(self, cell_count=500, infected_count=1, latent_prob=0.25, cycles_per_day=10,
                 infection_probability=0.25, infection_radius=10, infection_period=30,
                 latent_to_active_prob=0, infection_prob_latent=0.05, infection_prob_active=0.1,
                 cell_speed=0.5, death_probability=0, cell_size=3,
                 color_healthy=(127, 179, 213), color_latent=(255, 140, 255),
                 color_active=(255, 100, 100), color_dead=(0, 0, 0),
                 background_color=(0, 0, 0)):
        self.cell_count = cell_count
        self.infected_count = infected_count
        self.latent_prob = latent_prob
        self.cycles_per_day = cycles_per_day
        self.infection_probability = infection_probability
        self.infection_radius = infection_radius
        self.infection_period = infection_period
        self.latent_to_active_prob = latent_to_active_prob
        self.infection_prob_latent = infection_prob_latent
        self.infection_prob_active = infection_prob_active
        self.cell_speed = cell_speed
        self.death_probability = death_probability
        self.cell_size = cell_size
        self.color_healthy = color_healthy
        self.color_latent = color_latent
        self.color_active = color_active
        self.color_dead = color_dead
        self.background_color = background_color