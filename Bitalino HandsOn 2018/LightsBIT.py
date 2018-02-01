import bitalino

import numpy

# Mac OS
macAddress = "/dev/tty.BITalino-01-93-DevB"

# Windows
# macAddress = "XX:XX:XX:XX:XX:XX"

device = bitalino.BITalino(macAddress)

state = device.state()

toggle = 1-state['digitalChannels'][2]

device.trigger([toggle, 0])

print "LIGHTS ON" if toggle else "LIGHTS OFF"

device.close()
