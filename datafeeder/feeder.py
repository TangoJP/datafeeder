from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
import time
from datafeeder.datasource import SingleSource, MultiSource


class ABCFeeder(ABC):
    @abstractclassmethod
    def __init__(self):
        pass
    
    @abstractclassmethod
    def __iter__(self):
        pass
    
    @abstractclassmethod
    def __next__(self):
        pass

class SingleRowFeeder(ABCFeeder):
    def __init__(self, source, cols=[], num_feeds=10, retrieve_type='iloc',
                 print_col_names=False, **pandas_kwargs):
        """
        INPUT:
        ======
        source : str or DataFrame
            file path for data or DataFrame object
        cols : list
            columns to include
        num_feeds : positive int
            number of times to feed
        retrieve_type : str
            by default, it uses iloc[] for slicing, 
            but if this parameter is set to 'loc', use loc[]
        print_col_names : Boolean
            if True, print the included column names
        pandas_kwargs : dict
            **kwargs for pd.read_csv()
        
        ATTRIBUTES:
        ===========
        index : int
            index for the iterator
        source : Source() object
            Source object read from source input.
        """
        self.index = 0
        self.source = SingleSource(source, cols=cols, **pandas_kwargs)
        self.retrieve_type = retrieve_type

        if num_feeds > self.source.size:
            raise ValueError('num_feeds must not be bigger than the source size')
        self.num_feeds = num_feeds

        if print_col_names:
            print(self.source.column_names)

    def __iter__(self):
        return self
    
    def __next__(self):
        # Stop iteration once max reached
        if self.index >= self.num_feeds:
            raise StopIteration()
        
        # Retrieve data from source and feed
        data = self.source.retrieve_data(self.index, type=self.retrieve_type)
        self.index += 1
        return data


class MultiRowFeeder(SingleRowFeeder):
    def __init__(self, source, cols=[], num_rows=5, num_feeds=10, 
                 print_col_names=False, **pandas_kwargs):
        super().__init__(source, cols=cols, num_feeds=num_feeds,
                         print_col_names=False, **pandas_kwargs)
        self.num_rows = num_rows
    
    def __iter__(self):
        super().__iter__()

    def __next__(self):
        # Stop iteration once max reached
        if self.index >= (self.source.size - self.num_feeds):
            raise StopIteration()
        
        # Retrieve data from source and feed
        data = self.source.retrieve_data(self.index, num_rows=self.num_rows)
        self.index += 1
        return data


class MultiSourceFeeder(ABCFeeder):
    """
    Multi-version of Feeder
    """
    def __init__(self, sources, cols=[], num_feeds=10,
                 print_col_names=False, **pandas_kwargs):
        """
        INPUT:
        ======
        sources : dict
            sources input for MultiSources object
        cols : list
            list of columns to include
        num_feeds : int
            number of feeds
        print_col_names : Boolean
            print included column names or not
        pandas_kwargs : dict
            kwargs for pd.read_csv() function

        ATTRIBUTES:
        ===========
        index : int
            index for the Feeder
        """
        self.index = 0
        self.sources = MultiSource(sources, cols=cols, **pandas_kwargs)

        if any(num_feeds > size for size in self.sources.sizes.values()):
            raise ValueError('num_feeds must not be bigger than the source size')
        self.num_feeds = num_feeds

        if print_col_names:
            print(cols)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """
        next() method. Identical to Feeder class except what's returned is
        dictionary instead of tuple.
        """
        if self.index >= self.num_feeds:
                raise StopIteration()
            
        data = self.sources.retrieve_data(self.index)
        self.index += 1
        return data

# Use below for quick testing
if __name__ == '__main__':
    pass

### END