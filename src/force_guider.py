from __future__ import annotations
from numpy.typing import NDArray
import numpy as np
import time
from typing import Callable


class ForceGuider:
    def __init__(self, ramp: Callable[[float], float]) -> None:
        self.guiding_start_time = time.time()
        self.guiding_time = 0.0
        self.ramp = ramp

    def initiate_guiding_force(self, guide_time: float) -> bool:
        if time.time() - self.guiding_start_time < self.guiding_time:
            return False

        self.guiding_start_time = time.time()
        self.guiding_time = guide_time

        return True

    def modulate_force(self, F: float | NDArray) -> float | NDArray:
        t = 0.0 if self.guiding_time == 0.0 else (
            time.time() - self.guiding_start_time) / self.guiding_time
        modulation = self.ramp(t)
        return F * modulation
