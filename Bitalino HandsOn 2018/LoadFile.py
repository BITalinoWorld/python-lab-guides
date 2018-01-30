# -*- coding: utf-8 -*-
from pylab import *

data = loadtxt("SampleEMG.txt")

plot(data[:,5])
show()