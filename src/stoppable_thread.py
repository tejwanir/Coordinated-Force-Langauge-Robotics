from typing import Any, Callable, Dict, Optional
import threading
import traceback

class StoppableThread(threading.Thread):
    def __init__(
        self, 
        loop_method: Callable[[threading.Event, Dict[Any, Any]], None], 
        loop_method_args: Optional[Dict[Any, Any]] = None, 
        name: Optional[str] = None
    ):
        super().__init__(name=name)
        self.loop_method = loop_method
        self.loop_method_args = loop_method_args
        self.stop_event = threading.Event()

    def run(self):
        try:
            self.loop_method(self.stop_event, self.loop_method_args)
        except Exception as e:
            print(f'Error occurred in thread {self.name}: {e}')
            traceback.print_exc()
            self.stop_event.set()

    def stop(self):
        self.stop_event.set()