from multiprocessing import Process, Event

class StoppableProcess(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        """
        Initialize the stoppable process.
        """
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self._stop_event = Event()

    def stop(self):
        """
        Set the stop event to signal the process to terminate.
        """
        self._stop_event.set()

    def stopped(self):
        """
        Check if the stop event has been set.
        """
        return self._stop_event.is_set()