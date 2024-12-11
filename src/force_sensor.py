from optoforce import OptoForce22 as OptoForce
import numpy as np
from numpy.typing import NDArray


class ForceSensor:
    def __init__(self):
        raise NotImplementedError()

    def read(self) -> NDArray:
        raise NotImplementedError()


class OptoForceSensor(ForceSensor):
    FX_SCALE = 0.1 * 7925 / 300
    FY_SCALE = 0.1 * 8641 / 300
    FZ_SCALE = 0.1 * 6049 / 2000

    def __init__(self):
        self.sensor = OptoForce(zero=True)
        self.sensor.connect()

    def read(self) -> NDArray:
        measurement = self.sensor.read(only_latest_data=True)
        print(measurement.Fz * self.FZ_SCALE)
        return np.array([
            measurement.Fx * self.FX_SCALE,
            measurement.Fy * self.FY_SCALE,
            measurement.Fz * self.FZ_SCALE])

    def __del__(self):
        self.sensor.close()
