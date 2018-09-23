from datafeeder.plotter import Plotter, FeedPlotter
from datafeeder.feeder import SingleRowFeeder
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
            plotter.scatter(i, y, **scatter_kwargs)
        
        plt.show()

    def test_scatter_with_formatted_axis(self):
        plotter = Plotter(pause=0.5)
        self.assertIsInstance(plotter, Plotter)

        plotter.format_axis( 
            xlim=[-1, 11], ylim=[-0.1, 1.1],
            xlabel='Iteration', ylabel='Random #', 
            title='Basic Plotter Class Test with axis formatting'
        )
        
        num_points = 10
        scatter_kwargs = {'color':'skyblue', 'marker':'^'}
        for i in range(num_points):
            #print(i)
            y = np.random.random()
            plotter.scatter(i, y, **scatter_kwargs)
        
        plt.show()


class TestFeedPlotter(unittest.TestCase):

    def test_basic_scatter(self):
        # Set up plotter
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'

        # set up feeder
        num_feeds = 50
        feeder = SingleRowFeeder(
            source, cols=['time', 'close'], num_feeds=num_feeds, 
            print_col_names=False, parse_dates=['time'], 
            dtype={'close':np.float64}
        )

        # Set up plotter
        plotter = Plotter(pause=1e-12)
        plotter.format_axis(
                title='test scatter @ FeedPlotter',
                xlabel='time',
                ylabel='EUR/JPY',
                grid=True,
        )

        # scatter plot
        feedplotter = FeedPlotter(feeder, plotter)
        scatter_kargs = {'color':'skyblue', 's':10, 'marker':'s'}

        self.assertEqual(feedplotter.feeder.index, 0)
        feedplotter.scatter(**scatter_kargs)
        self.assertEqual(feedplotter.feeder.index, num_feeds)


if __name__ == '__main__':
    unittest.main()



### END