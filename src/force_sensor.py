from timer import Timer
from realtime_figure import RealtimeFigureWindow
from optoforce import OptoForce22 as OptoForce
import numpy as np
from numpy.typing import NDArray
from typing import Tuple


class ForceSensor:
    def __init__(self):
        raise NotImplementedError()

    def read(self) -> NDArray:
        raise NotImplementedError()


class OptoForceSensor(ForceSensor):
    FX_SCALE = 0.1 * 7925 / 300
    FY_SCALE = 0.1 * 8641 / 300
    FZ_SCALE = 0.1 * 6049 / 2000
    TX_SCALE = 0.1
    TY_SCALE = 0.1
    TZ_SCALE = 0.1

    def __init__(self):
        self.sensor = OptoForce(zero=True)
        self.sensor.connect()

    def read(self) -> Tuple[NDArray, NDArray]:
        measurement = self.sensor.read(only_latest_data=True)
        force = np.array([
            measurement.Fx * self.FX_SCALE,
            measurement.Fy * self.FY_SCALE,
            measurement.Fz * self.FZ_SCALE])
        torque = np.array([
            measurement.Tx * self.TX_SCALE,
            measurement.Ty * self.TY_SCALE,
            measurement.Tz * self.TZ_SCALE])
        return force, torque

    def __del__(self):
        self.sensor.close()


if __name__ == '__main__':
    figure = RealtimeFigureWindow(refresh_rate=100, subplot_options_set=[
        {'colors': ['red', 'green', 'blue']}])

    timer = Timer()
    sensor = OptoForceSensor()
    zero_force = sensor.read()
    force_axis = []
    t_axis = []

    while True:
        t = timer.t()
        force, torque = sensor.read()

        t_axis.append(t)
        force_axis.append(force)

        for options in figure.subplot_options_set:
            options['xlim'] = (t - 10, t)
            figure.update([(t_axis, force_axis)])
