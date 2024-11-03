from __future__ import annotations
from numpy.typing import NDArray
import numpy as np
import time
from typing import Callable


class ForceGuider:
    def __init__(self, ramp: Callable[[float], float], max_force: float = 30) -> None:
        self.guiding_start_time = time.time()
        self.guiding_time = 0.0
        self.ramp = ramp
        self.max_force = max_force

    def initiate_guiding_force(self, guide_time: float) -> bool:
        if time.time() - self.guiding_start_time < self.guiding_time:
            return False

        self.guiding_start_time = time.time()
        self.guiding_time = guide_time

        return True

    def get_modulation(self) -> float:
        t = 0.0 if self.guiding_time == 0.0 else (
            time.time() - self.guiding_start_time) / self.guiding_time
        modulation = self.ramp(t)
        return modulation

    def modulate_force(self, F: float | NDArray) -> float | NDArray:
        F_guide = F * self.get_modulation()

        if np.linalg.norm(F_guide) > self.max_force:
            F_guide *= self.max_force / np.linalg.norm(F_guide)

        return F_guide
