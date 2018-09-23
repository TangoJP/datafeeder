import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datafeeder.feeder import (
    ABCFeeder, SingleRowFeeder, MultiRowFeeder, MultiSourceFeeder)

class Plotter:
    """
    Class to create a plotter, that plots a point whose data are to be fed by
    a feeder.
    """
    @staticmethod
    def create_figure(figsize=(10, 6)):
        """
        Just creates a plain fig and ax objects using plt.subplots()

        INPUT:
        ======
        figsize : tuple
            figsize parameter for plt.subplots()
        
        OUTPUT:
        fig :
            matplotlib figure object
        ax :
            matplotlib axis object associated with fig
        """
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        return fig, ax

    def __init__(self, ax=None, pause=1e-12,
                 title='',xlabel='', ylabel='', grid=True,
                 xlim=None, ylim=None, **axis_kwargs):
        """
        Instantiation sets 'pause' parameter that sets the time interval 
        between plots. It also creates an axes.Axes object if not specified.
        """
        self.pause = pause
        if ax is None:
            self.fig, self.ax = self.create_figure()
        else:
            self.ax = ax

    def format_axis(self, title='',xlabel='', ylabel='', grid=True,
                    xlim=None, ylim=None, **axis_kwargs):
        """
        This function takes in a matplotlib axes.Axes object and formats it.
        """
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if xlim:
            self.ax.set_xlim(xlim)
        if ylim:
            self.ax.set_ylim(ylim)
        if grid and type(grid) == dict:
            self.ax.grid(grid)
        elif grid:
            self.ax.grid(color='0.7', ls=':')

    def scatter(self, x, y, **scatter_kwargs):
        """
        scatter plot a single point with a pause
        """
        plt.pause(self.pause)
        self.ax.scatter(x, y, **scatter_kwargs)
        

class FeedPlotter:
    
    def __init__(self, feeder, plotter):
        """
        INPUTS:
        feeder : iterable Feeder object
            Feeder object
        plotter : Plotter object
            Plotter object
        """
        if not isinstance(feeder, ABCFeeder):
            raise TypeError('feeder input must be a Feeder object')

        # Set up a Feeder
        self.feeder = feeder
        self.plotter = plotter
    
    def scatter(self, **scatter_kwargs):
        """
        Use Feeder object as an iterator and Plotter object as the plotter
        to plot each time point in the data.
        """
        for feed in self.feeder:
            self.plotter.scatter(feed[0], feed[1], **scatter_kwargs)
        plt.show()

### END