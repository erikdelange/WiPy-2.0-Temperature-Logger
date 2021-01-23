# WiPy Temperature Logger
Measure temperatures using DS18X20 1-Wire sensors and have a minimal webserver rendering a temperature chart.

### Summary
The DS18X20 family provides cheap 1-Wire temperature sensors. A single data line on the WiPy can be connected to multiple sensors. In this project two are used. A daemon process samples the data from these sensors every 30 seconds. A small webserver is started which always returns a page with a temperature chart over the last half hour. JavaScript library Chart.js is used to render the chart.

### Chart
![chart.png](https://github.com/erikdelange/WiPy-2.0-Temperature-Logger/blob/master/chart.png)

### Code
The lists (t0 and t1, one per sensor) which hold the temperature readings are pre-allocated. Also a list with labels (lbl, not shown on the graph, but anyhow mandatory) is prepared. The measurement daemon (a thread) sleeps most of the time, but wakes up every 30 seconds. A lock is used when the daemon updates the temperature lists as the webserver could be reading these lists at the same time. The webserver is the most simple variant possible: regardless what the clients requests it always returns a page with a chart. The chart displays the last 60 temperature readings (as the list never grows beyond this number).

##### Memory usage
I used a WiPy 2, so had to be conservative in memory consumption. The obvious approach of defining the full webpage upfront as a string and using format() to add the dynamic content caused memory fragmentation and eventually resulted in an out-of-memory exceptions and a crashed webserver. That is why the webpage is served in four smaller chunks, where only the content of the second part (html2; the data for the chart) is dynamically created. To send a relatively large static file (mychart.js) to the client I transmit in blocks of 512 bytes. By pre-allocating a 512 byte buffer and accessing this via a memoryview no hidden objects are created. If you want to see the memory status during execution uncomment the two lines with 'micropython'.

### Tools
Package onewire.py is copied from the Pycom documentation.
The DS18X20 works perfectly on 3.3V, but do not forget to place a 4K7 resistor between Vdd and the sensors data line. It does not matter how many sensors are connected to that data line.
Of course the WiPy must be visible in your network. See the Pycom documentation on how to setup WLAN.
