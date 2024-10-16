import numpy as np
from numpy.typing import NDArray


class UrgencyMeter:
    def __init__(self) -> None:
        self.alpha = 0.0

    def update(self, alignment: float | NDArray, dt: float) -> None:
        raise NotImplementedError()

    def get_urgency(self) -> float | NDArray:
        return self.alpha


class UrgencyMeterPID(UrgencyMeter):
    def __init__(self, K_p: float | NDArray, K_i: float | NDArray, K_d: float | NDArray, scale: float | NDArray = 1.0) -> None:
        super().__init__()
        self.K_p = K_p * scale
        self.K_i = K_i * scale
        self.K_d = K_d * scale
        self.A = 0.0
        self.int_A = 0.0
        self.dAdt = 0.0

    def update(self, alignment: float, dt: float, integral_reset_threshold: float | NDArray = 0.2) -> None:
        previous_A = self.A
        self.A = alignment
        self.dAdt = (self.A - previous_A) / dt
        self.int_A += self.A * dt

        self.int_A[abs(self.A) < integral_reset_threshold] = 0.0
        self.int_A[np.sign(previous_A) != np.sign(self.A)] = 0.0

        pid = self.K_p * self.A + self.K_i * self.int_A + self.K_d * self.dAdt
        self.alpha = 2.0 / (1.0 + np.exp(-pid)) - 1.0

    def reset_integral(self) -> None:
        self.int_A = 0.0
