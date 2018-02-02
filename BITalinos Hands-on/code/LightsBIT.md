# LightsBIT.py Step by step
1 - Import bitalino and numpy python libraries
```
import bitalino

import numpy
```

2 - Input your device's MAC address

```
# Mac OS
# macAddress = "/dev/tty.BITalino-01-93-DevB"

# Windows
macAddress = "XX:XX:XX:XX:XX:XX"

device = bitalino.BITalino(macAddress)
```
3 - Get your device's state. This will show information about the battery, the analog channels and the digital channels (IN and OUT).
More information (http://bitalino.com/pyAPI/index.html?highlight=state#bitalino.BITalino.state)

We are interested in the digital channels, which are numbered as: [IN 1, IN 2, OUT 1, OUT 2] = [0, 1, 2, 3]. 

LED light is located at OUT 1, so what is its state?

```
state = device.state()
print(state)
```

4 - Now we will switch the state of the LED light located at state\['digitalChannels'\]\[2\]. 

The toggle variable takes the desired value (1=ON, 0 OFF).

In case LED is ON, we switch to OFF. In case LED is OFF, we switch to ON

```
toggle = 1-state['digitalChannels'][2]
print (toggle)
```

5 - Let's trigger the Light switch
```
device.trigger([toggle, 0])
```
6 - Finally we print ON/OFF on screen according to the resulting illumination and close the access to the device

```
print ("LIGHTS ON") if toggle else ("LIGHTS OFF")

device.close()
```


