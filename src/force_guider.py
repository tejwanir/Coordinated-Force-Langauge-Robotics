from numpy.typing import NDArray
import numpy as np


class ForceGuider:
    def __init__(self) -> None:
        pass

    def get_guiding_force(self, F_human: float | NDArray, F_ideal: float | NDArray) -> float | NDArray:
        raise NotImplementedError()


class UrgencyForceGuider(ForceGuider):
    def __init__(self, decay_rate: float | NDArray = 32.0, guidance_strength: float = 8.0) -> None:
        super().__init__()

        self.alpha = 0.0
        self.dalphadt = 0.0
        self.beta = 0.0
        self.dbetadt = 0.0
        self.force = 0.0
        self.decay_rate = decay_rate
        self.guidance_strength = guidance_strength

    def update(self, urgency: float | NDArray, dt: float) -> None:
        previous_alpha = self.alpha
        self.alpha = urgency
        self.dalphadt = (self.alpha - previous_alpha) / dt

        self.dbetadt = self.alpha - self.decay_rate * self.beta
        self.beta += self.dbetadt * dt

    def get_guiding_force(self, F_human: float | NDArray, F_ideal: float | NDArray) -> float | NDArray:
        beta_max = 1.0 / self.decay_rate
        beta_norm = self.beta / beta_max

        weight = np.clip(beta_norm / (np.linalg.norm(F_human) + 1.0), 0.0, 1.0)
        F_guide = (1.0 - weight) * F_human + weight * F_ideal * self.guidance_strength - F_human
        return F_guide