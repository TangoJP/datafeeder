import numpy as np
import pandas as pd
import time
from datafeeder.timer.pulser import Pulser


class ABCTimer:
    pass


class Timer(ABCTimer):
    
    def __init__(self, period, interval=1, unit='min'):
        self.period = period
        self.interval = interval
        self.unit = unit
        
    
    def execute(self):
        pass


# For testing
if __name__ == "__main__":
    pass

