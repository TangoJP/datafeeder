# To be run from the directory with __main__()


from datafeeder.feeder.feeder import CSVFeeder
import pandas as pd
import unittest

def print_feed(i, pulse):
    print('{:d}-th pulse: {}'.format(i, pulse))

class TestCSVFeeder(unittest.TestCase):

    def test_dataframe_source(self):
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
        feeder.feed(num_feeds, print_feed)
        self.assertEqual(feeder.retrieve_next, num_feeds)

    def test_dataframe_source_specific_columns(self):
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
        feeder.feed(num_feeds, print_feed, cols=['time', 'close']) 
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
        feeder.feed(num_feeds, print_feed)
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
        feeder.feed(num_feeds, print_feed, cols=['open', 'high'])

        self.assertEqual(feeder.retrieve_next, num_feeds)
    
    def test_wait(self):
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
        feeder.feed(num_feeds, print_feed, wait=2)
        self.assertEqual(feeder.retrieve_next, num_feeds)

if __name__ == '__main__':
    unittest.main()

### END