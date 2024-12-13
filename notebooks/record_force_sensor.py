import sys
sys.path.append('src')  # nopep8

from force_sensor import OptoForceSensor
import pandas as pd
import time
import keyboard

sensor = OptoForceSensor()
force_axis = []
t_axis = []
last_keypress_time = 0
turn = 1
print(f'Turn {turn}')

data = []

try:
    while True:
        if keyboard.is_pressed('enter') and time.time() - last_keypress_time > 1:
            turn += 1
            print(f'Turn {turn}')
            last_keypress_time = time.time()

        force, torque = sensor.read()
        data.append([time.time(), turn, force[0], force[1], force[2],
                     torque[0], torque[1], torque[2]])
finally:
    data_frame = pd.DataFrame(
        columns=["time", "turn", "fx", "fy", "fz", "tx", "ty", "tz"], data=data)
    data_frame.to_csv(f'{time.time()}.csv')
