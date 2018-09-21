from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
import time

def read_source(source, **pandas_kwargs):
    if type(source) == str: # Read file as CSV
        df = pd.read_csv(source, **pandas_kwargs).reset_index(drop=True)
    elif type(source) == pd.core.frame.DataFrame:   # Directly assign
        df = source
    else:
        raise TypeError('\'source\' must be DataFrame or String.')

    return df


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


class MyFeeder1(AbstractFeeder):

    def __init__(self, source, **pandas_kwargs):
        self.source = read_source(source, **pandas_kwargs)
        
    def _retrieve_data(self):
            return super()._retrieve_data()
    
    def _feed_data(self):
            return super()._feed_data()
    
    def feed(self):
            return super().feed()

    def __iter__():
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
        self.df = read_source(source, **pandas_kwargs)

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
        if type(cols) != list:
            raise TypeError('cols must be a list (can be empty or single element list')
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

    def feed(self, num_feeds, cols=[], wait=0, yield_index=False):
        """
        Retrieve & feed multiple times using Pulser object. 'func' that should
        utilize the retrieved data is executed 'num_feeds' times. Time
        interval between feeds can be set with 'wait' parameter.

        INPUTS:
        =======
        num_feeds : int
            Number of times to feed
        cols : list
            columns to slice from DF
        wait : non-negative int/float
            time interval between feeds
        """
        while self.retrieve_next < num_feeds:
            time.sleep(wait)
            data = self._retrieve_and_feed(self.retrieve_next, cols=cols)
            if yield_index:
                yield self.retrieve_next, data
            else:
                yield data
            self.retrieve_next += 1


class MultiFeeder(AbstractFeeder):
    """
    sources = {name1:path1, name2:path2, ...}
    sources = {name1:df1, name2:df2, ...}

    cols = {name1:[col1, col2], name2:[col3, col4], ....}
    """
    def __init__(self, sources, **pandas_kwargs):
        # Check elements of sources
        if not isinstance(sources, dict):
            raise TypeError('sources must be a dictionary object')
        if all(isinstance(source, pd.core.frame.DataFrame) for source in sources.values()):
            self.sources = sources
        elif all(isinstance(source, str) for source in sources.values()):
            self.sources = {}
            for k, v in sources.items():
                self.sources[k] = pd.read_csv(v, **pandas_kwargs)
        else:
            raise TypeError('all values of the sources dictionary must be a str or DataFrame')



        pass

    def _retrieve_data(self):
        pass
    
    def _feed_data(self):
        pass

    def feed(self):
        pass



### END