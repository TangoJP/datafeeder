from datafeeder.feeder.feeder import CSVFeeder
import pandas as pd

source = [
    {'time':1, 'open':100, 'close':110},
    {'time':2, 'open':101, 'close':109},
    {'time':3, 'open':102, 'close':108},
    {'time':4, 'open':103, 'close':107},
    {'time':5, 'open':104, 'close':106}
]
source = pd.DataFrame(source)
print(type(source) == pd.core.frame.DataFrame)

feeder = CSVFeeder(source)

feeder.feed(5)


### END