# -*- coding: utf-8 -*-
from pylab import *
from biosppy.signals import ecg

data = loadtxt("SampleECG.txt")[:,-1]

out = ecg.ecg(signal=data, sampling_rate=1000., show=True)


# out = ecg.ecg(signal=data, sampling_rate=1000., show=False)

# raw = data-data.mean()
# filtered = out['filtered']-out['filtered'].mean()

# plot(raw)
# plot(filtered, 'k')

# vlines(out['rpeaks'], min(raw)*2, max(raw)*2, 'gray', 'dashed')

# legend(['raw', 'filtered', 'R-peaks'])
