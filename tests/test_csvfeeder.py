# To be run from the directory with __main__()


from datafeeder.feeder import CSVFeeder
import pandas as pd
import numpy as np
import unittest

# def print_feed(i, pulse):
#     print('{:d}-th pulse: {}'.format(i, pulse))

# def print_feed(df, i, cols):
#     print('{:d}-th pulse: {}'.format(i, df[cols].iloc[i]))

class TestCSVFeeder(unittest.TestCase):

    def test_pandas_import_kwargs(self):
        print('\n')
        print('Feeding from a file...')
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        feeder = CSVFeeder(
            source, parse_dates=['time'], dtype={'close':np.float64})
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertTrue(feeder.df['close'].dtype == np.float64)
        print(feeder.df['time'].dtype)
        #self.assertTrue(feeder.df['time'].dtype == np.datetime64)

    def test_dataframe_source(self):
        print('\n')
        print('Feeding from DataFrame directly...')
        source = [
            {'time':1, 'open':100, 'close':110},
            {'time':2, 'open':101, 'close':109},
            {'time':3, 'open':102, 'close':108},
            {'time':4, 'open':103, 'close':107},
            {'time':5, 'open':104, 'close':106}
        ]
        source = pd.DataFrame(source)
        feeder = CSVFeeder(source)
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertEqual(feeder.retrieve_next, 0)

        num_feeds = 5
        print('To feed {:d} times below:'.format(num_feeds))
        for feed in feeder.feed(num_feeds, yield_index=False):
            print(feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)

    def test_dataframe_source_specific_columns(self):
        print('\n')
        print('Feeding from DataFrame directly...')
        source = [
            {'time':1, 'open':100, 'close':110},
            {'time':2, 'open':101, 'close':109},
            {'time':3, 'open':102, 'close':108},
            {'time':4, 'open':103, 'close':107},
            {'time':5, 'open':104, 'close':106}
        ]
        source = pd.DataFrame(source)
        feeder = CSVFeeder(source)
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertEqual(feeder.retrieve_next, 0)

        num_feeds = 5
        print('To feed {:d} times below:'.format(num_feeds))
        for feed in feeder.feed(num_feeds, cols=['time','close'], yield_index=False):
            print(feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)

    def test_file_source(self):
        print('\n')
        print('Feeding from a file...')
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        feeder = CSVFeeder(source)
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertEqual(feeder.retrieve_next, 0)

        num_feeds = 5
        print('To feed {:d} times below:'.format(num_feeds))
        for feed in feeder.feed(num_feeds, yield_index=False):
            print(feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)

    def test_file_source_specific_columns(self):
        print('\n')
        print('Feeding from a file...')
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        feeder = CSVFeeder(source)
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertEqual(feeder.retrieve_next, 0)

        num_feeds = 5
        print('To feed {:d} times below:'.format(num_feeds))
        for feed in feeder.feed(num_feeds, cols=['time','close'], yield_index=False):
            print(feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)
    
    def test_wait(self):
        print('\n')
        print('Feeding from a file...')
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        feeder = CSVFeeder(source)
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertEqual(feeder.retrieve_next, 0)

        num_feeds = 5
        print('To feed {:d} times below:'.format(num_feeds))
        for feed in feeder.feed(num_feeds, cols=['time','close'], 
                                wait=1, yield_index=False):
            print(feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)

    def test_yield_index(self):
        print('\n')
        print('Feeding from a file...')
        source = './data/EURJPY/EURJPY_2002-201802_day.csv'
        feeder = CSVFeeder(source)
        self.assertTrue(type(feeder.df) == pd.core.frame.DataFrame)
        self.assertEqual(feeder.retrieve_next, 0)

        num_feeds = 5
        print('To feed {:d} times below:'.format(num_feeds))
        for feed in feeder.feed(num_feeds, cols=[], 
                                wait=0, yield_index=True):
            print(feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)

if __name__ == '__main__':
    unittest.main()

### END