# To be run from the directory with __main__()


from datafeeder.feeder import Source, Feeder, MultiSource, MultiFeeder
import pandas as pd
import numpy as np
import unittest


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
sources = {'src1':source1, 'src2':source2}

class TestSource(unittest.TestCase):
    
    def test_attributes(self):
        src = Source(source1, name='test1', cols=['time', 'close'])
        self.assertTrue(isinstance(src, Source))
        self.assertEqual(src.name, 'test1')
        self.assertSequenceEqual(src.column_names, ['time', 'close'])
        self.assertEqual(src.size, 5)
    
    def test_retrieve_row(self):
        src = Source(source1, name='test1', cols=['time', 'close'])
        data_0 = src.retrieve_row(0)
        self.assertSequenceEqual(data_0, (0, 101))


class TestFeeder(unittest.TestCase):

    def test_attributes(self):
        feeder = Feeder(source1, cols=['time', 'close'], num_feeds=5, print_col_names=True)
        self.assertTrue(isinstance(feeder, Feeder))
        self.assertEqual(feeder.index, 0)
        self.assertEqual(feeder.retrieve_type, 'iloc')
        self.assertEqual(feeder.num_feeds, 5)
    
    def test_iteration(self):
        print('\n')
        print('Testing Feeder')
        feeder = Feeder(source1, cols=['time', 'close'], num_feeds=5, print_col_names=True)
        self.assertEqual(feeder.index, 0)
        for feed in feeder:
            print(feed)
        self.assertEqual(feeder.index, 5)


class TestMultiSource(unittest.TestCase):

    def test_attributes(self):
        src = MultiSource(sources, name='test1', cols=['time', 'close'])
        self.assertTrue(isinstance(src, MultiSource))
        self.assertTrue(isinstance(src.sources, list))
        self.assertTrue(all(isinstance(s, Source) for s in src.sources))
    
    def test_retrieve_row(self):
        src = MultiSource(sources, name='test1', cols=['time', 'close'])
        data_0 = src.retrieve_row(0)
        self.assertSequenceEqual(data_0['src1'], (0, 101))
        self.assertSequenceEqual(data_0['src2'], (0, 121))


class TestMultiFeeder(unittest.TestCase):
    
    def test_attributes(self):
        feeder = MultiFeeder(sources, cols=['time', 'close'], 
                             num_feeds=5, print_col_names=True)
        self.assertTrue(isinstance(feeder, MultiFeeder))
        self.assertTrue(isinstance(feeder.sources, MultiSource))
        self.assertEqual(feeder.index, 0)
        self.assertEqual(feeder.num_feeds, 5)
    
    def test_iteration(self):
        print('\n')
        print('Testing MultiFeeder')
        feeder = MultiFeeder(sources, cols=['time', 'close'], 
                             num_feeds=5, print_col_names=True)
        self.assertEqual(feeder.index, 0)
        for feed in feeder:
            print(feed)
        self.assertEqual(feeder.index, 5)


if __name__ == '__main__':
    unittest.main()