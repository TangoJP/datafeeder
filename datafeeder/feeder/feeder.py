from abc import ABC, abstractclassmethod
from datafeeder.periodic.pulser import Pulser
import numpy as np
import pandas as pd
import time


class AbstractFeeder(ABC):

    @abstractclassmethod
    def _retrieve_data(self):
        pass
    
    @abstractclassmethod
    def _feed_data(self):
        pass

    @abstractclassmethod
    def feed(self):
        pass

class CSVFeeder(AbstractFeeder):
    """
    Feeder that retrieves data from a CSV file and outputs one row at a time.
    """
    def __init__(self, source, **pandas_kwargs):
        """
        INPUTS:
        =======
        source : str or DataFrame
            source of the data. If it's str, it reads the file in the path
            as csv. If it's a DataFrame, it gets taken directly.
        
        **pandas_kwargs : **kwargs
            kwargs for pd.read_cs(source, **pandas_kwargs)
        
        ATTRIBUTES:
        ===========
        df : DataFrame
            Imported DataFrame from source
        retrieve_next : int
            Index for the next data row to retrieve
        data_size : int
            Number of rows in df
        """
        if type(source) == str: # Read file as CSV
            self.df = pd.read_csv(source, **pandas_kwargs).reset_index(drop=True)
        elif type(source) == pd.core.frame.DataFrame:   # Directly assign
            self.df = source
        else:
            raise TypeError('\'source\' must be DataFrame or String.')

        self.retrieve_next = 0
        self.data_size = len(self.df)

    def _retrieve_data(self, i, cols=[]):
        """
        Retrieve the i-th row from self.df.

        INPUTS:
        =======
        i : int
            index of the data row
        cols : list
            list of columns to select in a DF
        """
        if i >= self.data_size:
            raise KeyError('Max index alreay reached.')

        # if cols != [], slice the DataFrame
        if cols != []:
            data = self.df[cols].iloc[i]
        else:
            data = self.df.iloc[i]

        return tuple(data)
    
    def _feed_data(self, data):
        """
        Feed data
        """
        return data

    def _retrieve_and_feed(self, i, cols=[]):
        """
        Retrieve data row and feed it.

        INPUTS:
        =======
        i : int
            index of the data row
        """
        return self._feed_data(self._retrieve_data(i, cols=cols))

    def feed(self, num_feeds, func, cols=[], wait=0,
             *func_args, **func_kwargs):
        """
        Retrieve & feed multiple times using Pulser object. 'func' that should
        utilize the retrieved data is executed 'num_feeds' times. Time
        interval between feeds can be set with 'wait' parameter.

        INPUTS:
        =======
        num_feeds : int
            Number of times to feed
        func : callable
            function to call in the Pulser object
        cols : list
            columns to slice from DF
        wait : non-negative int/float
            time interval between feeds
        *func_args & **func_kwargs :
            *args and **kwargs for func
        """
        pulser = Pulser(num_feeds, self._retrieve_and_feed, wait=wait)

        for i, pulse in pulser.pulse(self.retrieve_next, cols):
            func(i, pulse, *func_args, **func_kwargs)
            self.retrieve_next += 1


### END