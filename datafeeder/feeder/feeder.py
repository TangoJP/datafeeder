from abc import ABC, abstractclassmethod
from datafeeder.timer.pulser import Pulser
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
    def __init__(self, source, **pandas_kwargs):
        if type(source) == str:
            self.df = pd.read_csv(source, **pandas_kwargs).reset_index(drop=True)
        elif type(source) == pd.core.frame.DataFrame:
            self.df = source
        else:
            raise TypeError('\'source\' must be DataFrame or String.')
        self.retrieve_next = 0
        self.data_size = len(self.df)

    def _retrieve_data(self, i, cols=[]):
        if i >= self.data_size:
            raise KeyError('Max index alreay reached.')

        if cols != []:
            data = self.df[cols].iloc[i]
        else:
            data = self.df.iloc[i]
        return tuple(data)
    
    def _feed_data(self, data):
        return data

    def _retrieve_and_feed(self, i, cols):
        return self._feed_data(self._retrieve_data(i, cols))

    def feed(self, num_feeds, cols=[], wait=0):
        pulser = Pulser(
            num_feeds,
            self._retrieve_and_feed,
            wait=0
        )
        for i, pulse in pulser.pulse(self.retrieve_next, cols):
            print('{:d}-th pulse: {}'.format(i, pulse))
            self.retrieve_next += 1














### END