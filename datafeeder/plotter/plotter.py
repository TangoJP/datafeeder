import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datafeeder.feeder.feeder import CSVFeeder

class Plotter:

    @staticmethod
    def create_figure(figsize=(10, 6)):
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        return fig, ax

    @staticmethod
    def format_axis(ax, 
                    title='',xlabel='', ylabel='', 
                    xlim=None, ylim=None, **axis_kwargs):
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if xlim:
            ax.set_xlim(xlim)
        if ylim:
            ax.set_ylim(ylim)

    def plot_scatter(self, x, y, pause=0, ax=None, **scatter_kwargs):
        if ax is None:
            fig, ax = self.create_figure()
        
        ax.scatter(x, y, **scatter_kwargs)
        plt.pause(pause)


if __name__ == '__main__':
    plotter = Plotter()

    fig, ax = plotter.create_figure()
    plotter.format_axis(
        ax, xlim=[-1, 11], ylim=[-0.1, 1.1],
        xlabel='Iteration', ylabel='Random #', title='Plotter Class Test')

    num_points = 10
    pause = 0.5
    scatter_kwargs = {'color':'skyblue', 'marker':'^'}
    for i in range(num_points):
        y = np.random.random()
        plotter.plot_scatter(i, y, pause=pause, ax=ax, **scatter_kwargs)
    
    plt.show()