import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datafeeder.feeder import Feeder, MultiFeeder

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

    @staticmethod
    def format_axis(ax, title='',xlabel='', ylabel='', grid=True,
                    xlim=None, ylim=None, **axis_kwargs):
        """
        This function takes in a matplotlib axes.Axes object and formats it.
        """
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)
        if grid and type(grid) == dict:
            ax.grid(grid)
        elif grid:
            ax.grid(color='0.7', ls=':')

    def __init__(self, ax=None, pause=0,
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

    def plot_scatter(self, x, y, **scatter_kwargs):
        """
        scatter plot a single point with a pause
        """
        plt.pause(self.pause)
        self.ax.scatter(x, y, **scatter_kwargs)
        

class FeedPlotter:
    
    def __init__(self, source, num_feeds=10, retrieve_type='iloc', 
                 pause=1e-12, x=None, y=None, ax=None, 
                 title='',xlabel='', ylabel='', xlim=None, ylim=None,
                 grid=True, **pandas_kwargs):
        """
        INPUTS:
        source : str or DataFrame:
            path to a .csv file or pandas.DataFrame object
        num_feeds : int
            number of feeds to plot
        wait : positive int or float
            time interval between data retrieval. Same as interval btw plots
        x : str
            column name in the csv file / DF that goes to x-axis
        y : str
            column name in the csv file / DF that goes to y-axis
        ax : matplotlib axis object or None
            axis object to plot on. If None, it automatically generates a
            figure and an axis
        tilte : str
            title of the plot
        xlabel : str
            xlabel
        ylabel : str
            yabel
        xlim : list or None:
            limits on x-axis
        ylim : list or None
            limits on y-axis
        grid : Boolean or dict
            parameters for ax.grid()
        pandas_kwargs : dict
            kwargs for reading in the csv file
        
        ATTRIBUTES (*skip noting the obvious ones):
        ===========
        self.feeder : Feeder (iterable)
            Feeder object used to feed from CSV data read as DataFrame
        self.plotter : Plotter
            Plotter object used to plot the fed data.
        """
        # Set up a Feeder
        self.feeder = Feeder(source, cols=[x, y], 
                             num_feeds=num_feeds, retrieve_type='iloc', 
                             print_col_names=False, **pandas_kwargs)   

        # Set up a Plotter
        self.pause = pause
        self.plotter = Plotter(ax=None, pause=self.pause)
    
    def format_plotter_axis(self, title='',xlabel='', ylabel='', grid=True,
                            xlim=None, ylim=None, **axis_kwargs):
        """
        Format the axis using Plotter().format_axis(). This function was 
        separated from instantiation and plot(), so that different kinds of
        kwargs can go in at each point (i.e. kwargs for pandas, axes, and
        plt.scatter() functions.)
        """
        self.plotter.format_axis(
            ax=self.plotter.ax, 
            title=title, xlabel=xlabel, ylabel=ylabel,
            grid=grid, xlim=xlim, ylim=ylim, **axis_kwargs
        )

    def plot(self, **scatter_kwargs):
        """
        Use Feeder object as an iterator and Plotter object as the plotter
        to plot each time point in the data.
        """
        for feed in self.feeder:
            self.plotter.plot_scatter(feed[0], feed[1], **scatter_kwargs)
        plt.show()


### END