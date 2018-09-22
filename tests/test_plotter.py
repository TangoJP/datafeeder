from datafeeder.plotter import Plotter, FeedPlotter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unittest

class PlotterTest(unittest.TestCase):

    def test_basic_scatter(self):
        plotter = Plotter(pause=0.5)
        self.assertIsInstance(plotter, Plotter)
        num_points = 10
        scatter_kwargs = {'color':'skyblue', 'marker':'^'}
        for i in range(num_points):
            #print(i)
            y = np.random.random()
            plotter.plot_scatter(i, y, **scatter_kwargs)
        
        plt.show()

    def test_scatter_with_formatted_axis(self):
        plotter = Plotter(pause=0.5)
        self.assertIsInstance(plotter, Plotter)

        plotter.format_axis(
            plotter.ax, 
            xlim=[-1, 11], ylim=[-0.1, 1.1],
            xlabel='Iteration', ylabel='Random #', 
            title='Basic Plotter Class Test with axis formatting'
        )
        
        num_points = 10
        scatter_kwargs = {'color':'skyblue', 'marker':'^'}
        for i in range(num_points):
            #print(i)
            y = np.random.random()
            plotter.plot_scatter(i, y, **scatter_kwargs)
        
        plt.show()


class TestFeedPlotter(unittest.TestCase):

    def test_basic_scatter(self):
        # Set up plotter
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        num_feeds = 50
        plotter = FeedPlotter(source, num_feeds=num_feeds, pause=1e-12, 
                              x='time', y='close',
                              parse_dates=['time'], 
                              dtype={'close':np.float64})
        
        # Format axis
        plotter.format_plotter_axis(
        title='test_basic_scatter @ CSVPlotterTest',
        xlabel='time',
        ylabel='EUR/JPY',
        grid=True,
        )

        # scatter plot
        scatter_kargs = {'color':'skyblue', 's':10, 'marker':'s'}
        plotter.plot(**scatter_kargs)

    def test_counter(self):
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        num_feeds = 50
        plotter = FeedPlotter(source, num_feeds=num_feeds, pause=1e-12, 
                              x='time', y='close',
                              parse_dates=['time'], 
                              dtype={'close':np.float64})

        # Counter before plot should be set to 0    
        self.assertEqual(plotter.feeder.index, 0)
        plotter.plot()

        # Counter after plot should equal num_feeds
        self.assertEqual(plotter.feeder.index, num_feeds)


if __name__ == '__main__':
    unittest.main()



### END