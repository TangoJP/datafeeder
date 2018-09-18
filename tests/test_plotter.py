from datafeeder.plotter import plotter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unittest

class PlotterFunctionsTest(unittest.TestCase):

    def test_basic_scatter(self):
        # Create figure and an axis
        fig, ax = plotter.create_figure()

        num_points = 10
        pause = 2
        for i in range(num_points):
            y = np.random.random()
            plotter.plot_scatter(i, y, pause=pause, ax=ax)
        
        plt.show()




### END