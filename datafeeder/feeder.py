from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
import time


class Source:
    """
    Class to hold source data and allows access to the data by a retrieval
    method.
    """
    @staticmethod
    def read_source2df(source, **pandas_kwargs):
        """
        Function to read in or assigne 'source' into a DataFrame object.
        """
        if type(source) == str:     # Read file as CSV
            df = pd.read_csv(source, **pandas_kwargs).reset_index(drop=True)
        elif type(source) == pd.core.frame.DataFrame:   # Directly assign DF
            df = source
        else:
            raise TypeError('\'source\' must be DataFrame or String.')

        return df

    def __init__(self, source, name='', cols=[], **pandas_kwargs):
        """
        INPUTS:
        =======
        source : str or DataFrame
            if str, read in the file in the path, if DataFrame, directly
            assigns it as an attribute
        name : str
            name of the source
        cols : list
            list of columns to slice in the DataFrame
        pandas_kwargs: dict
            **kwargs for pd.read_csv() method

        ATTRIBUTES:
        ===========
        column_names : tuple
            tuple of the included columns

        """
        self.source = self.read_source2df(source, **pandas_kwargs)
        self.name = name
        self.size = len(source)
        if isinstance(cols, list) and cols != []:
            self.source = self.source[cols]
        if cols == []:
            self.column_names = tuple(self.source.columns)
        else:
            self.column_names = tuple(cols)

    def retrieve_row(self, ind, type='iloc'):
        """
        INPUT:
        ======
        ind : int
            index to retrieve
        type : 'iloc' or 'loc'
            typf of index retrieval to use. use iloc by default
        
        OUTPUT:
        =======
        returns DataFrame.iloc[ind] as tuple

        """
        if type == 'loc':
            return tuple(self.source.loc[ind])
        else:
            return tuple(self.source.iloc[ind])


class Feeder:
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
        # Stop iteration once max reached
        if self.index >= self.num_feeds:
            raise StopIteration()
        
        # Retrieve data from source and feed
        data = self.source.retrieve_row(self.index, type=self.retrieve_type)
        self.index += 1
        return data


class MultiSource:
    """
    Multi-version of Sources class
    """
    def __init__(self, sources, cols=[], **pandas_kwargs):
        """
        Input:
        ======
        sources : {name1:path1, name2:path2, ...} or {name1:df1, name2:df2, ...}
            dictionary whose key is the name of the data and the value the path
            to the file or DataFrame Object
        cols : list
            columns to include
        
        ATTRIBUTE:
        ==========
        sources : list
            list containig Source objects for sources input
        sizes : dictionary
            dict whose key is data name and the value the size of the data

        *in the future: cols = {name1:[col1, col2], name2:[col3, col4], ....}
        ** This assumes indices are aligned among different data. Also uses iloc[]
        """
        # Check elements of sources
        if not isinstance(sources, dict):
            raise TypeError('sources must be a dictionary object')
        self.sources = [Source(src, name=name, cols=cols) for name, src in sources.items()]
        self.sizes = {src.name:src.size for src in self.sources}

    def retrieve_row(self, ind):
        """
        Multi-version of retrieve_row() method of Source class. Returns
        {data_name:data_row} dictionary for .iloc[ind] position in each df
        """
        data = {
            src.name:src.retrieve_row(ind, type='iloc') for src in self.sources
        }
        return data


class MultiFeeder:
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
            
        data = self.sources.retrieve_row(self.index)
        self.index += 1
        return data

# Use below for quick testing
if __name__ == '__main__':
    pass

### END