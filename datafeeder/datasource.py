from abc import ABC, abstractclassmethod
import numpy as np
import pandas as pd
import time


class ABCDataSource(ABC):
    @abstractclassmethod
    def retrieve_data(self):
        pass

class SingleSource(ABC):
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
        self.size = len(self.source)
        if isinstance(cols, list) and cols != []:
            self.source = self.source[cols]
        if cols == []:
            self.column_names = tuple(self.source.columns)
        else:
            self.column_names = tuple(cols)

    def _retrieve_single_row(self, ind, type='iloc'):
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

    def _retrieve_rows(self, ind, num_rows):
        if (ind + num_rows) > self.size:
            raise IndexError('index max passed. \
                (\'ind + \' num_rows\') must be smaller than data size')
        
        data = [self._retrieve_single_row(i) for i in range(ind, ind + num_rows)]
        
        return data

    def retrieve_data(self, ind, num_rows=1, type='iloc'):
        if num_rows > 1:
            return self._retrieve_rows(ind, num_rows)
        else:
            return self._retrieve_single_row(ind, type=type)


class MultiSource(ABC):
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
        self.sources = [
            SingleSource(src, name=name, cols=cols)\
            for name, src in sources.items()]
        self.names = [src.name for src in self.sources]
        self.sizes = {src.name:src.size for src in self.sources}
    
    def retrieve_data(self, ind, num_rows=1):
        data = {
            src.name:src.retrieve_data(ind, num_rows=num_rows, type='iloc') \
            for src in self.sources
        }
        return data


# Use below for quick testing
if __name__ == '__main__':
    pass

### END