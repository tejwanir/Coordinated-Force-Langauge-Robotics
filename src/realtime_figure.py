from typing import List, Optional, Tuple, Dict, Any
from numbers import Number
from IPython.display import clear_output
import matplotlib
import matplotlib.axes
import matplotlib.lines
from matplotlib import pyplot as plt
import numpy as np

class RealtimeFigure:
    def _verify_mode(self, required_mode: str):
        if self.mode != required_mode:
            raise ValueError(f'Mode must be {required_mode} to run, not {self.mode}.')

    def __init__(self, rows: int = 1, columns: int = 1, subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None, mode: str = 'inline'):
        self.rows = rows
        self.columns = columns
        self.subplot_options_set = subplot_options_set
        self.mode = mode

        if self.mode == 'inline':
            self._init_inline_mode()
        elif self.mode == 'window':
            self._init_window_mode()

    def _init_inline_mode(self):
        self._verify_mode('inline')

        plt.switch_backend('inline')

    def _init_window_mode(self):
        self._verify_mode('window')

        plt.switch_backend('TkAgg')
        plt.ion()

        self._generate_subplots()

        self.fig.canvas.manager.window.wm_title("RealtimeFigure")

    def _generate_subplots(self):
        self.fig, axes = plt.subplots(self.rows, self.columns)
        self.axes = axes.ravel() if self.rows * self.columns > 1 else np.asarray([axes])

    def update(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        if self.mode == 'inline':
            self._generate_subplots()

        for i, (data_set, ax) in enumerate(zip(data_sets, self.axes)):
            if data_set == None:
                continue

            x, y = data_set

            ax.clear()

            lines = ax.plot(x, y, color='black')

            ax.grid(True)

            if self.subplot_options_set and self.subplot_options_set[i]:
                self._apply_subplot_options(ax, lines, self.subplot_options_set[i])

        self.fig.tight_layout()

        if self.mode == 'inline':
            self._render_inline_mode()
        elif self.mode == 'window':
            self._render_window_mode()

    def _apply_subplot_options(self, ax: matplotlib.axes.Axes, lines: List[matplotlib.lines.Line2D], subplot_options: Dict[str, Any]):
        subplot_option_methods = {
            "title": ax.set_title,
            "xlabel": ax.set_xlabel,
            "ylabel": ax.set_ylabel,
            "xlim": ax.set_xlim,
            "ylim": ax.set_ylim,
            "color": lambda colors: [line.set_color(color) for line, color in zip(lines, colors)]
        }

        for option, value in subplot_options.items():
            if option in subplot_option_methods:
                subplot_option_methods[option](value)

    def _render_inline_mode(self):
        self._verify_mode('inline')

        clear_output(wait=True)
        plt.show(block=False)
    
    def _render_window_mode(self):
        self._verify_mode('window')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()