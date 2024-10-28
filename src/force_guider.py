from __future__ import annotations
from numpy.typing import NDArray
import numpy as np
import time


class ForceGuider:
    def __init__(self) -> None:
        self.guiding_start_time = time.time()
        self.guiding_time = 0.0

    def initiate_guiding_force(self, guide_time: float) -> bool:
        if time.time() - self.guiding_start_time < self.guiding_time:
            return False

        self.guiding_start_time = time.time()
        self.guiding_time = guide_time

        return True

    def modulate_force(self, F: float | NDArray) -> float | NDArray:
        t = 0.0 if self.guiding_time == 0.0 else (
            time.time() - self.guiding_start_time) / self.guiding_time
        modulation = 0.0 if t > 1.0 else 1.0 - 4.0 * (t - 0.5) ** 2.0
        return F * modulation


class SimpleForceGuider:
    def __init__(self, a: float = 20.0, b: float = 2.0) -> None:
        self.a = a
        self.b = b

    def generate_guiding_force(self, F_error: float | NDArray, F_human: float | NDArray) -> float | NDArray:
        F_guide = F_error

        if np.linalg.norm(F_guide - F_human) > self.a:
            F_guide = F_guide / np.linalg.norm(F_guide) * self.a + F_human

        f_g, f_h = np.linalg.norm(F_guide), np.linalg.norm(F_human)
        if f_g > self.b * f_h:
            F_guide = F_guide / f_g * self.b * f_h

        return F_guide
