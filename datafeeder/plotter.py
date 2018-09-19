import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datafeeder.feeder import CSVFeeder

class Plotter:

    @staticmethod
    def create_figure(figsize=(10, 6)):
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        return fig, ax

    @staticmethod
    def format_axis(ax, title='',xlabel='', ylabel='', grid=True,
                    xlim=None, ylim=None, **axis_kwargs):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)
        if grid:
            ax.grid(color='0.7', ls=':')

    def __init__(self, ax=None, pause=0,
                 title='',xlabel='', ylabel='', grid=True,
                 xlim=None, ylim=None, **axis_kwargs):
        self.pause = pause

        if ax is None:
            self.fig, self.ax = self.create_figure()
        else:
            self.ax = ax
        
        self.format_axis(
            ax=self.ax, title=title, xlabel=xlabel, ylabel=ylabel,
            grid=grid, xlim=xlim, ylim=ylim, **axis_kwargs)

    def plot_scatter(self, x, y, **scatter_kwargs):
        self.ax.scatter(x, y, **scatter_kwargs)
        plt.pause(self.pause)


class CSVPlotter:
    
    def __init__(self, source, num_feeds, wait=1e-12,
                 x=None, y=None, ax=None, 
                 title='',xlabel='', ylabel='', xlim=None, ylim=None,
                 grid=True, **pandas_kwargs):
        
        self.csvfeeder = CSVFeeder(source, **pandas_kwargs)    # Set up a Feeder
        self.num_feeds = num_feeds
        self.wait = wait    # Time interval between feeds

        # Get data for x and y axes
        if x is None or y is None:
            raise ValueError('x and y cannot be None.')
        if type(x) != str or type(y) != str:
            raise TypeError('x and y must be str type.')
        if not (x in self.csvfeeder.df.columns and y in self.csvfeeder.df.columns):
            raise KeyError('x and y must be columns of the DataFrame')

        self.x = x
        self.y = y

        # Set up a Plotter
        self.plotter = Plotter(
            pause=self.wait, xlim=xlim, ylim=ylim,
            grid=grid, xlabel=xlabel, ylabel=ylabel, title=title
        )
        
    def plot(self, **scatter_kwargs):
        for feed in self.csvfeeder.feed(self.num_feeds,
                                        cols=[self.x, self.y],
                                        wait=self.wait):
            #print(feed[0], feed[1])
            self.plotter.plot_scatter(feed[0], feed[1], **scatter_kwargs)
        plt.show()

if __name__ == '__main__':
    source = './data/EURJPY/EURJPY_2002-201802_day.csv'
    plotter = CSVPlotter(source, 400, wait=1e-12, x='time', y='close',
                parse_dates=['time'], dtype={'close':np.float64})
    scatter_kargs = {'color':'skyblue', 's':10, 'marker':'s'}
    plotter.plot(**scatter_kargs)

### END