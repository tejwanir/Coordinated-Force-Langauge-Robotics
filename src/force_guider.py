from numpy.typing import NDArray
import numpy as np


class ForceGuider:
    def __init__(self) -> None:
        pass

    def get_guiding_force(self, F_human: float | NDArray, F_ideal: float | NDArray) -> float | NDArray:
        raise NotImplementedError()


class UrgencyForceGuider(ForceGuider):
    def __init__(self, decay_rate: float | NDArray = 1.0) -> None:
        super().__init__()

        self.alpha = 0.0
        self.dalphadt = 0.0
        self.beta = 0.0
        self.dbetadt = 0.0
        self.force = 0.0
        self.decay_rate = decay_rate

    def update(self, urgency: float | NDArray, dt: float) -> None:
        previous_alpha = self.alpha
        self.alpha = urgency
        self.dalphadt = (self.alpha - previous_alpha) / dt

        self.dbetadt = self.alpha - self.decay_rate * self.beta
        self.beta += self.dbetadt * dt

    def get_guiding_force(self, F_human: float | NDArray, F_ideal: float | NDArray) -> float | NDArray:
        beta_max = 1.0 / self.decay_rate
        beta_norm = self.beta / beta_max

        F_guide =  max(beta_norm, 0.0) * (8 * F_ideal - F_human) * max(1.0 - self.alpha, 0.0)
        return F_guide