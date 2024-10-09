from IPython.display import clear_output
from matplotlib import pyplot as plt

class LivePlotter:
    def plot(self, x, y):
        clear_output(wait=True)
        plt.figure()
        plt.plot(x, y)
        plt.show()