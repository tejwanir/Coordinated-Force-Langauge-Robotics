import time

class Timer:
    def __init__(self) -> None:
        self.start_time = time.time()
        self.t = 0.0
    
    def dt(self) -> float:
        new_t = time.time() - self.start_time
        dt = new_t - self.t
        self.t = new_t
        return dt
    
    def get_t(self) -> float:
        return self.t