from typing import List, Optional, Tuple, Dict, Any
from numbers import Number
from matplotlib import pyplot as plt
import numpy as np
from IPython.display import clear_output
from timer import Timer

class RealtimeFigure:
    def __init__(
        self,
        rows: int = 1,
        columns: int = 1,
        subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None,
        refresh_rate: int = 10,
    ):
        for name, value in [('rows', rows),
                            ('columns', columns)]:
            if not isinstance(value, int) or value < 1:
                raise ValueError(f'Invalid value for {name}: {value}. Must be a counting number.')
            
        if refresh_rate <= 0:
            raise ValueError(f'Invalid value for refresh rate: {refresh_rate}. Must be a positive number.')

        self.rows = rows
        self.columns = columns
        self.subplot_options_set = subplot_options_set
        self.refresh_rate = refresh_rate
        self.initialized = False
        self.timer = Timer()

    def subplots_num(self):
        return self.rows * self.columns

    def init_subplots(self):
        self.fig, axes = plt.subplots(self.rows, self.columns)
        self.axes = axes.ravel() if self.subplots_num() > 1 else np.asarray([axes])

    def update_subplots(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        for i, (data_set, ax) in enumerate(zip(data_sets, self.axes)):
            if data_set == None:
                continue

            x, y = data_set

            ax.clear()

            if len(x) != len(y):
                raise ValueError(f'x and y must have the same length, but got {len(x)} and {len(y)} respectively.')

            lines = ax.plot(x, y, color='black')

            ax.grid(True)

            if self.subplot_options_set and i < len(self.subplot_options_set) and self.subplot_options_set[i]:
                subplot_option_methods = {
                    "title": ax.set_title,
                    "xlabel": ax.set_xlabel,
                    "ylabel": ax.set_ylabel,
                    "xlim": ax.set_xlim,
                    "ylim": ax.set_ylim,
                    "colors": lambda colors: [line.set_color(color) for line, color in zip(lines, colors)]
                }

                for option, value in self.subplot_options_set[i].items():
                    if option in subplot_option_methods:
                        subplot_option_methods[option](value)

        self.fig.tight_layout()

    def update(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        if self.timer.t() < 1 / self.refresh_rate:
            return

        self.timer.reset()
            
        if not self.initialized:
            self.initialize()
            self.initialized = True
        self.pre_update_hook()
        self.update_subplots(data_sets)
        self.render()

    def initialize(self):
        pass

    def pre_update_hook(self):
        pass

    def render(self):
        raise NotImplementedError("Subclasses should implement the render method.")

class RealtimeFigureInline(RealtimeFigure):
    def initialize(self):
        plt.switch_backend('module://matplotlib_inline.backend_inline')

    def pre_update_hook(self):
        self.init_subplots()

    def render(self):
        clear_output(wait=True)
        plt.show(block=False)

class RealtimeFigureWindow(RealtimeFigure):
    def initialize(self):
        plt.switch_backend('TkAgg')
        plt.ion()
        self.init_subplots()
        self.fig.canvas.manager.window.wm_title("RealtimeFigure")

    def render(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

_mode_to_realtime_figure_subclass_map: Dict[str, RealtimeFigure] = {
    'inline': RealtimeFigureInline,
    'window': RealtimeFigureWindow,
}

_modes = set(_mode_to_realtime_figure_subclass_map.keys())

_modes_string = ', '.join(f"'{mode}'" for mode in _modes)

def create(
        rows: int = 1,
        columns: int = 1,
        subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None,
        refresh_rate: int = 10,
        mode: str = 'inline',
    ) -> RealtimeFigure:
    if mode in _mode_to_realtime_figure_subclass_map:
        return _mode_to_realtime_figure_subclass_map[mode](rows, columns, subplot_options_set, refresh_rate)
    else:
        raise ValueError(f"Unsupported mode '{mode}' received. Supported modes are: {_modes_string}.")