# To be run from the directory with __main__()


from datafeeder.datasource import SingleSource, MultiSource
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

class TestSingleSource(unittest.TestCase):
    
    def test_attributes(self):
        src = SingleSource(source1, name='test1', cols=['time', 'close'])
        self.assertTrue(isinstance(src, SingleSource))
        self.assertEqual(src.name, 'test1')
        self.assertSequenceEqual(src.column_names, ['time', 'close'])
        self.assertEqual(src.size, 5)
    
    def test_retrieve_row(self):
        src = SingleSource(source1, name='test1', cols=['time', 'close'])
        data_0 = src.retrieve_data(0)
        self.assertSequenceEqual(data_0, (0, 101))

    def test_retrieve_rows(self):
        src = SingleSource(source1, name='test1', cols=['time', 'close'])
        ind = 0
        num_rows = 3
        data_03 = src.retrieve_data(ind, num_rows)
        self.assertTrue(isinstance(data_03, list))
        self.assertEqual(len(data_03), num_rows)
        self.assertSequenceEqual(data_03[0], (0, 101))
        self.assertSequenceEqual(data_03[1], (1, 105))
        self.assertSequenceEqual(data_03[2], (2, 102))


class TestMultiSource(unittest.TestCase):

    def test_attributes(self):
        src = MultiSource(sources, cols=['time', 'close'])
        self.assertTrue(isinstance(src, MultiSource))
        self.assertTrue(isinstance(src.sources, list))
        self.assertTrue(all(isinstance(s, SingleSource) for s in src.sources))
        self.assertSequenceEqual(src.names, ['src1', 'src2'])

    def test_retrieve_row(self):
        src = MultiSource(sources, cols=['time', 'close'])
        data_0 = src.retrieve_data(0)
        self.assertSequenceEqual(data_0['src1'], (0, 101))
        self.assertSequenceEqual(data_0['src2'], (0, 121))

    def test_retrieve_rows(self):
        src = MultiSource(sources, cols=['time', 'close'])
        ind = 0
        num_rows = 3
        data_03 = src.retrieve_data(ind, num_rows)
        self.assertTrue(isinstance(data_03, dict))
        self.assertEqual(len(data_03), 2)
        self.assertEqual(len(data_03['src1']), num_rows)
        self.assertEqual(len(data_03['src2']), num_rows)
        self.assertSequenceEqual(data_03['src1'][0], (0, 101))
        self.assertSequenceEqual(data_03['src1'][1], (1, 105))
        self.assertSequenceEqual(data_03['src1'][2], (2, 102))
        self.assertSequenceEqual(data_03['src2'][0], (0, 121))
        self.assertSequenceEqual(data_03['src2'][1], (1, 125))
        self.assertSequenceEqual(data_03['src2'][2], (2, 122))


if __name__ == '__main__':
    unittest.main()