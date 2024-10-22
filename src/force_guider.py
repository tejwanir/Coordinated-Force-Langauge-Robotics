from __future__ import annotations
from numpy.typing import NDArray
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
