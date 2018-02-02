import bitalino

import numpy

# Mac OS
macAddress = "/dev/tty.BITalino-01-93-DevB"

# Windows
# macAddress = "XX:XX:XX:XX:XX:XX"

device = bitalino.BITalino(macAddress)

while True:
    state = device.state()
    
    toggle = state['digitalChannels'][0]
    
    device.trigger([toggle, 0])
    
    device.battery(0 if toggle else 63)
    
    print "LIGHTS ON" if toggle else "LIGHTS OFF"

device.close()
