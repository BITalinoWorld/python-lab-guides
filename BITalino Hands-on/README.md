![Header](images/bitalinoheader.jpg)
*BITalino Python lab guide based on the workshop materials created by Hugo Silva. 
Adapted by Miquel Alfaras and Hugo Gamboa.*

[0. Setting up](#settingup)  
[1. Acquisition](#acq)  
[2. Opening Recorded Data in Python](#opensignal)  
[3. Post-Processing a Signal](#process)  
[4. Analyzing your Data](#analize)  
[5. Asynchronous Measurement and Control](#measure)  
[6. Real-Time Signal Processing](#online)  
[7. Live on the Web Browser](#browser)  
[8. External Links](#external)  
  
[A. Installation Notes (Python)](#installationnotes)


![bar](images/bitalinobar.jpg)
##  0. Setting up <a name="settingup"></a>
- Install the Anaconda Python distribution that best suits your platform (Python 2.7 is recommended):  
 https://www.anaconda.com/download/

- Install the BITalino Python API (recommended):  
https://github.com/BITalinoWorld/revolution-python-api

- Install BITalino's ServerBIT (r)evolution:    
https://github.com/BITalinoWorld/revolution-python-serverbit

- Install OpenSignals (r)evolution Software:  
http://bitalino.com/en/software

- Install the BioSPPy Toolbox (may come in handy):  
https://github.com/PIA-Group/BioSPPy

- Get a good code editor:  

    - **Spyder** is already included with Anaconda *or*

    - **PyCharm** https://www.jetbrains.com/pycharm/  

- Enjoy executing some code (e.g. by launching a Jupyter notebook)

- Prepare your device by connecting the battery (i.e. slide the battery connector onto the white socket on the BITalino block labelled as PWR) 

- Turn your device on by sliding the power button to the ON position; a white LED will start fading in / out, meaning that the device is in standby

- Get familiar with the architecture of **BITalino** ([datasheet](http://bitalino.com/datasheets/REVOLUTION_BITalino_Board_Kit_Datasheet.pdf))

![IMAGE ALT TEXT](images/BITalino_cut.jpg)


![bar](images/bitalinobar.jpg)
## 1. Acquisition <a name="acq"></a>

Once your BITalino is turned on, pair the device with your computer via the Bluetooth device manager using the PIN `1234` (this is a one-time process). Your device will be named `BITalino-XX-XX`, with `XX-XX` being the last four hex digits of your devices' MAC address.

**IMPORTANT NOTE:** The MAC address is the sequence `XX:XX:XX:XX:XX:XX` found on the label on the back of the devices' BT block and / or on the back of the cardboard packaging where the device is shipped.

The following steps should guide you through to a first glimpse of your signals in real-time:

- Launch **OpenSignals (r)evolution**

- Enable your device for acquisition by pressing the magnifying glass icon on the main screen and clicking the box showing the MAC address of your device (this is a one-time process)  
  **IMPORTANT NOTE:** The ENABLE button needs to be blue  

- You can proceed directly to record data, but you can also use this screen to configure the acquisition settings for your device (e.g. select the channels to be acquired, identify the type of sensor or change the sampling rate)  

- It is recommended that you review the sensor datasheets to obtain instructions regarding the typical electrode placement, sensor specifications and the transfer functions that can be used to convert the raw data into the correct physical units:
    - [Electromyography (EMG)](http://bitalino.com/datasheets/REVOLUTION_EMG_Sensor_Datasheet.pdf) 

    - [Electrodermal Activity (EDA)](http://bitalino.com/datasheets/REVOLUTION_EDA_Sensor_Datasheet.pdf) 

    - [Electrocardiography (ECG)](http://bitalino.com/datasheets/REVOLUTION_ECG_Sensor_Datasheet.pdf) 

    - [Electroencephalography (EEG)](http://bitalino.com/datasheets/EEG_Sensor_Datasheet.pdf) 

    - [Accelerometry (ACC)](http://bitalino.com/datasheets/REVOLUTION_ACC_Sensor_Datasheet.pdf) 

    - [Optical Sensing (LUX)](http://bitalino.com/datasheets/REVOLUTION_LUX_Sensor_Datasheet.pdf) 

    - [Event Annotation (BTN)](http://bitalino.com/datasheets/REVOLUTION_BTN_Sensor_Datasheet.pdf) 

- **Record a signal** by pressing the red circle on the main menu of the software  


![IMAGE ALT TEXT](images/opensig.jpg)
![bar](images/bitalinobar.jpg)
## 2. Opening Recorded Data in Python <a name="opensignal"></a>

Locate a recording on your hard drive; for your convenience, we provide the [SampleACC.txt](SampleACC.txt) file with a snippet of Accelerometry (ACC) data.

You can make a simple experiment using the Python script [LoadFile.py](LoadFile.py); this code uses the function [loadtxt](https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.loadtxt.html) (in this case made available through the `PyLab` module), to load the recorded data onto a variable in your program and display it in a graphic:
```python
from pylab import *

data = loadtxt("SampleACC.txt")

plot(data[:,5])
```

![IMAGE ALT TEXT](images/ACC_Plot.png)  

Use this code in Spyder or in a Jupyter notebook (an annotated notebook version of this script can be seen at [LoadFile_steps.ipynb](detailed/LoadFile_steps.ipynb)).

**IMPORTANT NOTE:** In the `SampleACC.txt` file, ACC data was recorded using the BITalino analog input `A5`, and can be found on column `6` of the file; given that Python uses zero-based numbering for indexing, the data matrix is being sliced in column `5` (i.e. `data[:,5]`). Further information about the content of the files recorded using OpenSignals (r)evolution can be found at: http://forum.bitalino.com/viewtopic.php?f=15&t=481&p=1553#p1553  


![bar](images/bitalinobar.jpg)
## 3. Post-Processing a Signal <a name="process"></a>

Based on the previous code, another experiment you can do is to compute the envelope of the EMG signal (i.e. smooth the absolute value of the signal after removing the mean).

To facilitate this task, you can use the Python script [ProcessFile.py](ProcessFile.py), which loads an EMG signal sample in order to remove its baseline and apply a low-pass filter to it:

```python
from pylab import *
from numpy import *
from scipy import signal

def lowpass(s, f, order=2, fs=1000.0):
    b, a = signal.butter(order, f / (fs/2))
    return signal.lfilter(b, a, s)

data = loadtxt("SampleEMG.txt")

emg_data = data[:,5]

abs_data = abs(emg_data-mean(emg_data))

proc_data = lowpass(abs_data, 10) # filter with a lowpass filter at 10Hz

plot(emg_data)

plot(proc_data)
```

![IMAGE ALT TEXT](images/EMG_Plot.png)  


![bar](images/bitalinobar.jpg)
## 4. Analyzing your Data <a name="analize"></a>

Python is often referred to as "the batteries included language", meaning that there are plenty of useful modules either bundled or contributed by the community. Biosignals are no exception and some libraries already bundle basic signal processing and analytics components. 

One experiment you can do, is to extract the heartbeat waveforms and determine the instant heart rate for an ECG signal using the BioSPPy toolbox. To facilitate this task, you can use the Python script [AnalyzeFile.py](AnalyzeFile.py), which loads an ECG signal sample in order to filter it, extract several convenient features and plot them in a chart:

```python
from pylab import *
from biosppy.signals import ecg

data = loadtxt("SampleECG.txt")[:,-1]

out = ecg.ecg(signal=data, sampling_rate=1000., show=True)

```  
![IMAGE ALT TEXT](images/ECG_Summary.png)

In the previous example, the toolbox is used in a more automated manner to take in raw data and produce a graphical output. However, you also have the possibility to access the extracted features and manipulate them directly. The following experiment demonstrates just that; the raw data is processed using the toolbox, plotted against the filtered version and annotated with vertical lines placed on the positions of the R-peaks.

```python
from pylab import *
from biosppy.signals import ecg

data = loadtxt("SampleECG.txt")[:,-1]

out = ecg.ecg(signal=data, sampling_rate=1000., show=False)

raw = data-data.mean()
filtered = out['filtered']-out['filtered'].mean()

plot(raw)
plot(filtered, 'k')

vlines(out['rpeaks'], min(raw)*2, max(raw)*2, 'gray', 'dashed')

legend(['raw', 'filtered', 'R-peaks'])
```
![IMAGE ALT TEXT](images/ECG_Plot.png)  


![bar](images/bitalinobar.jpg)
## 5. Asynchronous Measurement and Control <a name="measure"></a>

Until now we've seen how to work with data recorded using OpenSignals (r)evolution in post-processing tasks, however, it is also possible to interact with the device directly from your Python program.

The BITalino MCU supports multiple operation modes (detailed in the [datasheet](http://bitalino.com/datasheets/REVOLUTION_MCU_Block_Datasheet.pdf)), which are conveniently exposed through user-friendly high-level methods provided on the [APIs](http://bitalino.com/en/development/apis). Our experiments will use the [Python API](https://github.com/BITalinoWorld/revolution-python-api), for which documentation is available here:
http://bitalino.com/pyAPI/

The example [LightsBIT.py](LightsBIT.py) (shown bellow) demonstrates how to read and change the [state](http://bitalino.com/pyAPI/#bitalino.BITalino.state) of the device. Whenever the program is executed, the LED actuator and the low battery indicator LED will turn ON if they were turned off and turn OFF otherwise, printing its state on screen.

To control the LED actuator, the [trigger](http://bitalino.com/pyAPI/#bitalino.BITalino.trigger) method is used, while the [battery](http://bitalino.com/pyAPI/#bitalino.BITalino.battery) method is used to obtain and change the low battery level threshold in such a way that the LED turns on or off.

An annotated notebook version of this script is available at [LightsBIT_steps.ipynb](detailed/LightsBIT_steps.ipynb)

**IMPORTANT NOTE:** You need to adapt the code so that the `macAddress` variable has the correct value for your operating system and device MAC address.

```python
import bitalino
import numpy

# Mac OS
# macAddress = "/dev/tty.BITalino-XX-XX-DevB"

# Windows
macAddress = "XX:XX:XX:XX:XX:XX"
 
device = bitalino.BITalino(macAddress)

state = device.state()

toggle = 1-state['digitalChannels'][2]

device.trigger([toggle, 0])

device.battery(0 if toggle else 63)

print ("LIGHTS ON" if toggle else "LIGHTS OFF")

device.close()
```

In the previous example, only when the program is executed an action is produced. Combining the same principles with a repetition structure introduces us to a more interactive behaviour.

This is illustrated on our [ButtonBIT.py](ButtonBIT.py) example (shown bellow), where a loop continuously checks the [state](http://bitalino.com/pyAPI/#bitalino.BITalino.state) of the device and turns the LED actuator and low battery LED ON or OFF, based on the state of the Pushbutton (BTN) sensor.

By default, the BTN sensor is connected to the BITalino digital input `I1` (hence the fetching of `state['digitalChannels'][0]`), and depending on whether the button is pressed, the abovementioned LEDs will turn ON or OFF accordingly.

An annotated version notebook of this script can be seen at [ButtonBIT_steps.ipynb](detailed/ButtonBIT_steps.ipynb)

```python 
import bitalino
import numpy

# Mac OS
# macAddress = "/dev/tty.BITalino-XX-XX-DevB"

# Windows
macAddress = "XX:XX:XX:XX:XX:XX"
 
device = bitalino.BITalino(macAddress)

try:
  while True:
      state = device.state()
      
      toggle = state['digitalChannels'][0]
      
      device.trigger([toggle, 0])
      
      device.battery(0 if toggle else 63)
      
      print ("LIGHTS ON" if toggle else "LIGHTS OFF")

finally:
  device.close()

```


![bar](images/bitalinobar.jpg)
## 6. Real-Time Signal Processing <a name="online"></a>

In the previous section we have seen how to asynchronously interface with BITalino from within a Python program. A big downside of asynchronous communication is the fact that the time in-between readings (i.e. sampling interval) is variable. 

Although many informal applications can cope with this operation model, for digital signal processing and research use it is of utmost importance to have a known and accurate sampling interval. For this reason, BITalino provides an operation mode where data is streamed at a fixed sampling rate.

Our [MuscleBIT.py](MuscleBIT.py) example (shown bellow) illustrates this operation mode. The streaming process is initiated by calling the [start](http://bitalino.com/pyAPI/#bitalino.BITalino.start) method, in which a sampling rate and set of channels to be acquired can be specified.

Once the device starts streaming, it is fundamental that the program reads the samples sent by the device in a timely and continuous (or near-continuous) manner, otherwise it will stop streaming automatically. In our example, this is achieved by putting the call to the [read](http://bitalino.com/pyAPI/#bitalino.BITalino.read) method inside a repetition structure.

This particular example computes the EMG signal envelope in real-time and turns the Buzzer (BUZ) actuator on in case a certain threshold is exceeded. Pressing the BTN sensor for a few seconds will stop the program. 

An annotated version notebook of this script can be seen at [MuscleBIT_steps.ipynb](detailed/MuscleBIT_steps.ipynb).

**IMPORTANT NOTE:** This is a time-critical operation and BITalino has a small internal buffer to accumulate samples (roughly less than 2 seconds), reason for which if the time in-between calls to the `read` method is much higher than the rate at which the device is streaming data (e.g. due to the time taken by calculations) the internal buffer will fill and the device will stop streaming data. A crucial component in this process is the amount of samples acquired from the device at a time; for additional information please refer to: http://forum.bitalino.com/viewtopic.php?t=129#p227

```python
import bitalino
import numpy
import time

# Mac OS
# macAddress = "/dev/tty.BITalino-XX-XX-DevB"

# Windows
macAddress = "XX:XX:XX:XX:XX:XX"
   
device = bitalino.BITalino(macAddress)
time.sleep(1)

srate = 1000
nframes = 100
threshold = 5

device.start(srate, [0])
print ("START")

try:
    while True:

        data = device.read(nframes)
        
        if numpy.mean(data[:, 1]) < 1: break

        EMG = data[:, -1]
        
        envelope = numpy.mean(abs(numpy.diff(EMG)))

        if envelope > threshold:
            device.trigger([0, 1])
        else:
            device.trigger([0, 0])

finally:
    print ("STOP")
    device.trigger([0, 0])
    device.stop()
    device.close()
```


![bar](images/bitalinobar.jpg)
## 7. Live on the Web Browser <a name="browser"></a>

Struggling with data acquisition in Python? We've handled part of the heavy load for you by creating [ServerBIT](https://github.com/BITalinoWorld/revolution-python-serverbit), an easy-to-install software bundle that runs in a service-like manner, continuously streaming data from the device to third-party applications (e.g. your web browser).

Once installed, you need to configure the MAC address and channels to be acquired through the [config.json](https://github.com/BITalinoWorld/revolution-python-serverbit#settings-in-configjson) by following the instructions described here:  
https://github.com/BITalinoWorld/revolution-python-serverbit#pre-configured-installers

ServerBIT runs in a resilient manner, meaning that once it is launched it will automatically attempt to connect to your configured device and, even if the device is not turned on or the connection is lost, it will periodically attempt to reconnect and resume the data streaming process. 

Data is streamed using [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) technology, helping you receive the data stream even in a web browser. 

With the ServerBIT running, if you open the [ClientBIT.html](https://github.com/BITalinoWorld/revolution-python-serverbit/blob/master/ClientBIT.html) sample web page (source code shown bellow) the signals from the sensor connected to channel `A1` will be displayed in real time. 

The `ClientBIT.html` user interface is implemented using open technologies, namely `HTML/CSS/JavaScript`, with graphics managed using the [Flot](http://www.flotcharts.org/flot/examples/basic-options/index.html) library, so feel free to scavange the web and fiddle with the source code to adapt it to your particular ideas.

```html
<html>
    <script language="javascript" type="text/javascript" src="jquery.js"></script> 
    <script language="javascript" type="text/javascript" src="jquery.flot.js"></script> 
    <script type="text/javascript">
        // Establish a connection to the ServerBIT
        var ws = new WebSocket("ws://localhost:9001/");
        ws.onopen = function() {
        };
        // Process the responses sent by the ServerBIT
        ws.onmessage = function (e) {
            data = JSON.parse(e.data)
            var d1 = [];
            ch = 'A1'
            for (var i = 0; i < data[ch].length; i += 1)
                d1.push([i, data[ch][i]]);
            $.plot($("#placeholder"), [ d1 ], {yaxis: {min:0, max: 1024}});
        };
        // Detect when the page is unloaded or close
        window.onbeforeunload = function() {
            ws.onclose = function () {};
            ws.close()
        };        
        
    </script>
    <body>
        <div><h1>BITalinoWS</h1></div>
	<div id="placeholder" style="width:600px;height:300px;"></div> 
    </body>
</html>
```


![bar](images/bitalinobar.jpg)
## 8. External Links <a name="external"></a>

- BITalino Forum allows you to learn, share and discuss your experiences with others:   
  http://forum.bitalino.com/

- BITalino Python API documentation is available here:  
  http://bitalino.com/pyAPI/

- BITalino APIs for several other languages can be found at:  
  http://bitalino.com/en/development/apis

- BioSPPy toolbox documentation is available here:  
  http://biosppy.readthedocs.io/en/stable/  
  
- BITalinoWorld channel on YouTube has a few nifty videos:  
  https://www.youtube.com/user/BITalinoWorld/videos

- [PLUX](https://www.plux.info) and [biosignalsplux](http://www.biosignalsplux.com/) have solutions that enable you to extend your research


![bar](images/bitalinobar.jpg)
## A. Installation Notes <a name="installationnotes"></a>

### Python 2.7

#### Windows

1. Install [Anaconda **Python 2.7**](https://www.anaconda.com/download/)  
   
2. Install the BITalino API and its dependencies by typing the following on a `Command Line` window:  
```
pip install bitalino
```  

3. Download the [BITalino API](https://github.com/BITalinoWorld/revolution-python-api) and move `bitalino.py` to a working directory of yours or add the containing folder to the `PYTHONPATH manager` on Spyder  

4. Run `bitalino.py` (e.g. with a Jupyter notebook test file); you should see data collected by BITalino printed on the console
 
    
#### Mac OS  

1. Install [Anaconda **Python 2.7**](https://www.anaconda.com/download/)  
       
2. Install the BITalino API and its dependencies by typing the following on a `Terminal.app` window:  
```
conda install bitalino
```  

3. Test `LightsBIT.py` (e.g. with a Jupyter notebook test file); you should see the LED actuator turning ON or OFF  


### Python 3

#### Windows
    
1. Install [Anaconda **Python 3**](https://www.anaconda.com/download/)  
       
2. Install `PySerial` for Python 3 from:  
   https://pypi.python.org/pypi/pyserial/3.0  
       
3. Install `PyBluez` for Python 3 from  
   https://pypi.python.org/pypi/PyBluez  
       
4. Download the [BITalino API](https://github.com/BITalinoWorld/revolution-python-api) and move `bitalino.py` to a working directory of yours or add the containing folder to the `PYTHONPATH manager` on Spyder  
    
5. Test `bitalino.py` (e.g. with a Jupyter notebook test file); you should see data collected by BITalino printed on the console

#### Mac OS

1. Install [Anaconda **Python 3**](https://www.anaconda.com/download)  
       
2. Install the BITalino API and its dependencies by typing the following on a `Terminal.app` window:    
```
conda install bitalino
```  
       
3. Test `LightsBIT.py` (e.g. with a Jupyter notebook test file); you should see the LED actuator turning ON or OFF  


<!--
### On Windows (for Python 3)

1. Install Anaconda3-4.2.0 (most recent with Python 3.5) according to your system from: 
    https://repo.continuum.io/archive/

2. Install dependencies
    ```bash
    pip install pyserial
    ```

3. Download and install old PyBluez (3.5) package wheel for the user platform (e.g. WinX64), not available from PyBluez PyPi resources
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pybluez
PyBluez‑0.22‑cp35‑none‑win_amd64.whl
    ```bash
    pip install PyBluez-0.22-cp35-none-win_amd64.whl
    ```

4. Create a folder called `revolution-python-api`

5. Download the BITalino API `.zip` and extract the files into the created folder called `revolution-python-api`
    https://github.com/BITalinoWorld/revolution-python-api/archive/master.zip

6. Test `bitalino.py` (e.g. with a Jupyter notebook test file); you should see data collected by BITalino printed on the console


### On Windows (for Python 2)

1. Install Anaconda 2.7 version 
    https://repo.continuum.io/archive/

2. Install dependencies
    ```bash
    pip install pyserial
    ```
  
3. Download and install old PyBluez (2.7) package wheel for the user platform (e.g. WinX64), not available from PyBluez PyPi resources
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pybluez
PyBluez‑0.22‑cp27‑none‑win_amd64.whl
    ```bash
    pip install PyBluez-0.22-cp27-none-win_amd64.whl
    ```


4. Install the BITalino API
    ```bash
    pip install bitalino
    ```

5. Test `LightsBIT.py` (e.g. with a Jupyter notebook test file); you should see the LED actuator turning ON or OFF


### On Mac OS (for Python 2)

1. Install Anaconda2.7 from: https://repo.continuum.io/archive/

2. Install PySerial dependency
    ```bash
    conda install -c conda-forge pyserial
    ```  
    
3. Install the BITalino API
    ```
    pip install bitalino
    ```

4. Test `LightsBIT.py` (e.g. with a Jupyter notebook test file); you should see the LED actuator turning ON or OFF

-->


