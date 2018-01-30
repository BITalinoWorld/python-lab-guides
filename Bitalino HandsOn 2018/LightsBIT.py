# -*- coding: utf-8 -*-
import bitalino

import numpy

macAddress = "/dev/tty.BITalino-60-88-DevB"

device = bitalino.BITalino(macAddress)

state = device.state()

toggle = 1-state['digitalChannels'][2]

print "LIGHTS ON" if toggle else "LIGHTS OFF"

device.close()
