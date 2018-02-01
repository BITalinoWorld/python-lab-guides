from pylab import *
from numpy import *
from scipy import signal

def lowpass(s, f, order=2, fs=1000.0):
    b, a = signal.butter(order, f / (fs/2))
    return signal.lfilter(b, a, s)

data = loadtxt("SampleEMG.txt")[:,5]

abs_data = abs(data)

proc_data = lowpass(abs_data, 10) #Filter with a lowpass filter at 10Hz

plot(data)

plot(proc_data)

show()