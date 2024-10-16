import os
import time

class Vocalizer:
    def __init__(self, buffer_period: float = 0.5) -> None:
        self.buffer_period = buffer_period
        self.last_utter_time = time.time() - buffer_period

    def utter(self, phrase: str, interupt: bool = False) -> None:
        if interupt:
            os.system(f'killall say; say "{phrase}" &')
            self.last_utter_time = time.time()
        elif time.time() - self.last_utter_time >= self.buffer_period:
            os.system(f'pgrep say || say "{phrase}" &')
            self.last_utter_time = time.time()
        
