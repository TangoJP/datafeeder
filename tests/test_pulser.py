# The second import fails unless run from the datafeeder (project root) directory
import time
from datafeeder.timer.pulser import Pulser

# Simple test func
def myprint1(message):
    return ('{}'.format(str(message) + '\n'))

def myprint2(message, wait):
    if type(wait) not in (int, float):
        raise TypeError('\'wait\' must be a number (int or float)')
    elif wait < 0:
            raise ValueError('num_pulses must be a positive number')
    
    time.sleep(wait)
    return myprint1(message)

def collect_pulse(pulse):
    print('{:d}-th: {}'.format(pulse[0], str(pulse[1])))

message = 'testing pulser'
pulser1 = Pulser(5, myprint1, wait=1)
pulser2 = Pulser(3, myprint2)
for pulse in pulser1.pulse(message):
    collect_pulse(pulse)