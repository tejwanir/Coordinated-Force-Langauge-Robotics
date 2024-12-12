import sys
sys.path.append('src')  # nopep8

from force_sensor import OptoForceSensor
import pandas as pd
import time

sensor = OptoForceSensor()
force_axis = []
t_axis = []

data = []

try:
    while True:
        force, torque = sensor.read()
        data.append([time.time(), force[0], force[1], force[2],
                     torque[0], torque[1], torque[2]])
finally:
    data_frame = pd.DataFrame(
        columns=["time", "fx", "fy", "fz", "tx", "ty", "tz"], data=data)
    data_frame.to_csv(f'{time.time()}.csv')
