import random
from cell_state import CellState

class Cell:
    MAX_SPEED = 2.0
    SPEED_CHANGE_FACTOR = 0.01
    current_day = 0  # Should ideally be managed externally.

    def __init__(self, x, y, speed, size=3, infection_period=10):
        self._x = x
        self._y = y
        self._speed_x = random.uniform(-speed, speed)
        self._speed_y = random.uniform(-speed, speed)
        self._state = CellState.HEALTHY
        self._infection_start_day = -1
        self.speed = speed
        self.size = size
        self.infection_period = infection_period
        self.randomize_movement = True

    # Properties for encapsulation
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = max(0, value)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = max(0, value)

    @property
    def state(self):
        return self._state

    @property
    def infection_start_day(self):
        return self._infection_start_day

    def set_state(self, new_state):
        valid_transitions = {
            CellState.HEALTHY: [CellState.ACTIVE, CellState.LATENT],
            CellState.ACTIVE: [CellState.LATENT, CellState.DEAD],
            CellState.LATENT: [CellState.ACTIVE],
            CellState.DEAD: [],
        }
        if new_state not in valid_transitions[self._state]:
            raise ValueError(f"Invalid state transition: {self._state} to {new_state}")

        self._state = new_state
        if new_state == CellState.ACTIVE:
            self._infection_start_day = Cell.current_day
        else:
            self._infection_start_day = -1

    def is_active(self):
        return self._state != CellState.DEAD

    def move(self, width, height):
        if not self.is_active():
            return

        # Update speed with random changes if randomization is enabled
        if self.randomize_movement:
            self._speed_x += random.uniform(-self.SPEED_CHANGE_FACTOR, self.SPEED_CHANGE_FACTOR)
            self._speed_y += random.uniform(-self.SPEED_CHANGE_FACTOR, self.SPEED_CHANGE_FACTOR)

        # Clamp speed
        self._speed_x = max(-self.MAX_SPEED, min(self._speed_x, self.MAX_SPEED))
        self._speed_y = max(-self.MAX_SPEED, min(self._speed_y, self.MAX_SPEED))

        # Update position
        self._x += self._speed_x
        self._y += self._speed_y

        # Handle boundaries with bounce
        if self._x <= 0 or self._x >= width:
            self._speed_x = -self._speed_x
            self._x = max(0, min(self._x, width))

        if self._y <= 0 or self._y >= height:
            self._speed_y = -self._speed_y
            self._y = max(0, min(self._y, height))

    def update_infection(self, death_probability, latent_to_active_probability):
        if self._state == CellState.LATENT:
            if random.random() < latent_to_active_probability:
                self.set_state(CellState.ACTIVE)
        elif self._state == CellState.ACTIVE:
            if Cell.current_day - self.infection_start_day >= self.infection_period:
                self.set_state(CellState.LATENT)
            elif random.random() < death_probability:
                self.set_state(CellState.DEAD)

    # State transition helpers
    def transition_to_healthy(self):
        self.set_state(CellState.HEALTHY)

    def transition_to_active(self):
        self.set_state(CellState.ACTIVE)

    def transition_to_latent(self):
        self.set_state(CellState.LATENT)

    def transition_to_dead(self):
        self.set_state(CellState.DEAD)
