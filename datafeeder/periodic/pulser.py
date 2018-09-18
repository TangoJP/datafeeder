import numpy as np
import pandas as pd
import time


class Pulser:
    """
    It executes a function for a fixed number of times and yields
    its result along with an index. It is basically an enumerator of a sort.
    """
    def __init__(self, num_pulses, func, wait=0):
        """
        INPUTS:
        =======
        num_pulses : int
            number of pulses to be emitted
        func : callable
            function to execute at each pulse

        ATTRIBUTES:
        self.num_pulses : int
            number of pulses
        self.func : callable
            function to execute
        self.counter : int
            total number of pulses emmitted by the Pulser object
        """
        # Raise TypeError if num_pulses are not an integer
        if type(num_pulses) != int:
            raise TypeError('num_pulses must be an \'int\' type')
        elif num_pulses < 0:
            raise ValueError('num_pulses must be a positive number')

        self.num_pulses = num_pulses
        self.func = func
        
        # Raise Error if wait not correctly specified
        if type(wait) not in (int, float):
            raise TypeError('\'wait\' must be a number (int or float)')
        elif wait < 0:
                raise ValueError('num_pulses must be a positive number')
        self.wait = wait

        self.counter = 0

    def pulse(self, *func_args, **func_kwargs):
        """
        This creates a iteractor object that yields i-th iteration
        index as well as whatever the input function returns

        INPUTS:
        *func_args & **func_kwargs: *args, **kwargs
            *args, **kwargs for self.func
        """
        for i in range(self.num_pulses):
            time.sleep(self.wait)
            yield i, self.func(*func_args, **func_kwargs)
            self.counter += 1   # counter for initial run would equal to i

    def reset_counter(self):
        """
        Resets the counter attribute to zero
        """
        self.counter = 0

### END