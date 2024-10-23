from typing import List, Optional, Tuple, Dict, Any
from numbers import Number
from matplotlib import pyplot as plt
import numpy as np
from IPython.display import clear_output

class RealtimeFigure:
    def __init__(
        self,
        rows: int = 1,
        columns: int = 1,
        subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None,
    ):
        for name, value in [('rows', rows),
                            ('columns', columns)]:
            if not isinstance(value, int) or value < 1:
                raise ValueError(f"Invalid value for '{name}': {value}. Must be a counting number.")

        self.rows = rows
        self.columns = columns

        self.subplot_options_set = subplot_options_set if subplot_options_set is not None else []

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

            if len(x) == 0 or len(y) == 0:
                continue

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

    def render(self):
        raise NotImplementedError("Subclasses should implement the render method.")

    def update(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        self.update_subplots(data_sets)
        self.render()

class RealtimeFigureInline(RealtimeFigure):
    def __init__(
        self,
        rows: int = 1,
        columns: int = 1,
        subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None,
    ):
        super().__init__(rows, columns, subplot_options_set)
        plt.switch_backend('module://matplotlib_inline.backend_inline')

    def render(self):
        clear_output(wait=True)
        plt.show(block=False)

    def update(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        self.init_subplots()
        super().update(data_sets)

class RealtimeFigureWindow(RealtimeFigure):
    def __init__(
        self,
        rows: int = 1,
        columns: int = 1,
        subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None,
    ):
        super().__init__(rows, columns, subplot_options_set)
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
        mode: str = 'inline'
    ) -> RealtimeFigure:
    if mode in _mode_to_realtime_figure_subclass_map:
        return _mode_to_realtime_figure_subclass_map[mode](rows, columns, subplot_options_set)
    else:
        raise ValueError(f"Unsupported mode '{mode}' received. Supported modes are: {_modes_string}.")