from timer import Timer

class AppLoop:
    def __init__(self) -> None:
        self.timer = Timer()
        self.running = False

    def startup(self) -> None:
        pass
    
    def update(self, t: float, dt: float) -> None:
        pass
    
    def shutdown(self) -> None:
        pass
    
    def stop(self) -> None:
        self.running = False
    
    def run(self) -> None:
        self.running = True
        self.startup()
        self.timer.reset()

        try:
            while self.running:
                t = self.timer.t()
                dt = self.timer.dt()
                self.update(t, dt)
        finally:
            self.shutdown()