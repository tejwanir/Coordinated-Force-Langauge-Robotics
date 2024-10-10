from typing import List, Optional, Tuple
from numbers import Number
from IPython.display import clear_output
from matplotlib import pyplot as plt
import numpy as np

class RealtimeFigure:
    def __init__(self, rows=1, columns=1, subplot_options=None):
        self.rows = rows
        self.columns = columns
        self.subplot_options = subplot_options

    def update(self, data_sets: List[Optional[Tuple[List[Number], List[Number]]]]):
        clear_output(wait=True)
        _, axes = plt.subplots(self.rows, self.columns)
        axes = axes.ravel() if self.rows * self.columns > 1 else np.asarray([axes])
        for i, data_set in enumerate(data_sets):
            if data_set == None:
                continue
            x, y = data_set
            axes[i].plot(x, y)
        plt.show()