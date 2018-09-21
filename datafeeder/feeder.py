from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
import time


class Source:
    @staticmethod
    def read_source2df(source, **pandas_kwargs):
        if type(source) == str:                         # Read file as CSV
            df = pd.read_csv(source, **pandas_kwargs).reset_index(drop=True)
        elif type(source) == pd.core.frame.DataFrame:   # Directly assign DF
            df = source
        else:
            raise TypeError('\'source\' must be DataFrame or String.')

        return df

    def __init__(self, source, name='', cols=[], **pandas_kwargs):
        self.source = self.read_source2df(source, **pandas_kwargs)
        self.name = name
        self.size = len(source)
        if isinstance(cols, list) and cols != []:
            self.source = self.source[cols]
        self.column_names = tuple(self.source.columns)

    def retrieve_row(self, ind, type='iloc'):
        if type == 'loc':
            return tuple(self.source.loc[ind])
        else:
            return tuple(self.source.iloc[ind])

class Feeder:
    def __init__(self, source, cols=[], num_feeds=10, retrieve_type='iloc',
                 print_col_names=False, **pandas_kwargs):
        """
        retrieve_type : str
            By default, it uses iloc[] for slicing, 
            but if this parameter is set to 'loc', use loc[] 
        """
        self.index = 0
        self.source = Source(source, cols=cols, **pandas_kwargs)
        self.retrieve_type = retrieve_type

        if num_feeds > self.source.size:
            raise ValueError('num_feeds must not be bigger than the source size')
        self.num_feeds = num_feeds

        if print_col_names:
            print(self.source.column_names)

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= self.num_feeds:
            raise StopIteration()
        
        data = self.source.retrieve_row(self.index, type=self.retrieve_type)
        self.index += 1
        return data


class MultiSouces:
    """
    sources = {name1:path1, name2:path2, ...}
    sources = {name1:df1, name2:df2, ...}
    cols = [col1, col2, ...]

    *in the future: cols = {name1:[col1, col2], name2:[col3, col4], ....}
    ** This assumes indices are aligned among different data. Also uses iloc[]
    """
    def __init__(self, sources, cols=[], **pandas_kwargs):
        # Check elements of sources
        if not isinstance(sources, dict):
            raise TypeError('sources must be a dictionary object')
        self.sources = [Source(src, name=name, cols=cols) for name, src in sources.items()]
        self.sizes = {src.name:src.size for src in self.sources}

    def retrieve_row(self, ind):
        data = {
            src.name:src.retrieve_row(ind, type='iloc') for src in self.sources
        }
        return data


class MultiFeeder:
    def __init__(self, sources, cols=[], num_feeds=10,
                 print_col_names=False, **pandas_kwargs):
        self.index = 0
        self.sources = MultiSouces(sources, cols=cols, **pandas_kwargs)

        if any(num_feeds > size for size in self.sources.sizes.values()):
            raise ValueError('num_feeds must not be bigger than the source size')
        self.num_feeds = num_feeds

        if print_col_names:
            print(cols)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= self.num_feeds:
                raise StopIteration()
            
        data = self.sources.retrieve_row(self.index)
        self.index += 1
        return data

# Use below for quick testing
if __name__ == '__main__':
    source1 = [
        {'time': 0, 'open':100, 'close': 101},
        {'time': 1, 'open':101, 'close': 105},
        {'time': 2, 'open':104, 'close': 102},
        {'time': 3, 'open':103, 'close': 101},
        {'time': 4, 'open':102, 'close': 107}
    ]
    source2 = [
        {'time': 0, 'open':120, 'close': 121},
        {'time': 1, 'open':121, 'close': 125},
        {'time': 2, 'open':124, 'close': 122},
        {'time': 3, 'open':123, 'close': 121},
        {'time': 4, 'open':122, 'close': 127}
    ]
    source1 = pd.DataFrame(source1)
    source2 = pd.DataFrame(source2)

    # Test single Feeder
    print("Testing Single Feeder")
    myfeeder1 = Feeder(source1, cols=['time', 'close'], num_feeds=5, print_col_names=True)
    for feed in myfeeder1:
        print(feed)

    # Test MultiFeeder
    print('\n')
    print("Testing MuliFeeder")
    sources = {'src1':source1, 'src2':source2}
    myfeeder2 = MultiFeeder(sources, cols=['time', 'close'], num_feeds=5)
    for feed in myfeeder2:
        print(feed)
### END