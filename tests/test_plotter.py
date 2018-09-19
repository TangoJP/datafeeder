from datafeeder.plotter import Plotter, CSVPlotter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unittest

class PlotterFunctionsTest(unittest.TestCase):

    def test_basic_scatter(self):
        plotter = Plotter(
            pause=0.5,
            xlim=[-1, 11], ylim=[-0.1, 1.1],
            xlabel='Iteration', ylabel='Random #', 
            title='Plotter Class Test')
        self.assertIsInstance(plotter, Plotter)

        num_points = 10
        scatter_kwargs = {'color':'skyblue', 'marker':'^'}
        for i in range(num_points):
            #print(i)
            y = np.random.random()
            plotter.plot_scatter(i, y, **scatter_kwargs)
        
        plt.show()


class CSVPlotterFunctionsTest(unittest.TestCase):

    def test_basic_scatter(self):
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        plotter = CSVPlotter(source, 100, wait=1e-12, x='time', y='close',
                    parse_dates=['time'], dtype={'close':np.float64})
        scatter_kargs = {'color':'skyblue', 's':10, 'marker':'s'}
        plotter.plot(**scatter_kargs)

    def test_counter(self):
        pass
        
if __name__ == '__main__':
    unittest.main()



### END