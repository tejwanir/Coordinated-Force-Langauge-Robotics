from typing import Any, Callable, Dict, Optional
import threading
import traceback

class StoppableThread(threading.Thread):
    def __init__(
        self, 
        stoppable_method: Callable[[threading.Event, Dict[Any, Any]], None], 
        stoppable_method_args: Optional[Dict[Any, Any]] = None, 
        name: Optional[str] = None
    ):
        super().__init__(name=name)
        self.stoppable_method = stoppable_method
        self.stoppable_method_args = stoppable_method_args
        self.stop_event = threading.Event()

    def run(self):
        try:
            self.stoppable_method(self.stop_event, self.stoppable_method_args)
        except Exception as e:
            print(f'Error occurred in thread {self.name}: {e}')
            traceback.print_exc()
            self.stop_event.set()

    def stop(self):
        self.stop_event.set()