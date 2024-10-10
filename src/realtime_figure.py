from typing import List, Optional, Tuple, Dict, Any
from numbers import Number
from IPython.display import clear_output
import matplotlib
from matplotlib import pyplot as plt
import numpy as np

class RealtimeFigure:
    def __init__(self, rows: int = 1, columns: int = 1, subplot_options_set: Optional[List[Optional[Dict[str, Any]]]] = None):
        self.rows = rows
        self.columns = columns
        self.subplot_options_set = subplot_options_set

    def update(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        clear_output(wait=True)

        _, axes = plt.subplots(self.rows, self.columns)
        axes = axes.ravel() if self.rows * self.columns > 1 else np.asarray([axes])

        for i, (data_set, ax) in enumerate(zip(data_sets, axes)):
            if data_set == None:
                continue

            x, y = data_set

            ax.clear()
            ax.plot(x, y)

            if self.subplot_options_set and self.subplot_options_set[i]:
                self._apply_subplot_options(ax, self.subplot_options_set[i])

        plt.tight_layout()
        plt.show()

    def _apply_subplot_options(self, ax: matplotlib.axes.Axes, subplot_options: Dict[str, Any]):
        subplot_option_methods = {
            "title": ax.set_title,
            "xlabel": ax.set_xlabel,
            "ylabel": ax.set_ylabel,
            "xlim": ax.set_xlim,
            "ylim": ax.set_ylim,
        }

        for option, value in subplot_options.items():
            if option in subplot_option_methods:
                subplot_option_methods[option](value)