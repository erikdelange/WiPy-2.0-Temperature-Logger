# WiPy Temperature Logger
Measure temperatures using DS18X20 1-Wire sensors and have a minimal webserver rendering a temperature chart.

### Summary
The DS18X20 family offers cheap 1-Wire temperature sensors. A single data line on the WiPy can be connected to multiple sensors. In this project two are used. A daemon proces samples the data from these sensors every 30 seconds. A small webserver is started which always returns a page with a temperature chart over the last half hour. JavaScript library Chart.js is used to render the chart.

### Chart
![](https://github.com/erikdelange/WiPy-2.0-Temperature-Logger/blob/master/chart.png)

### Code
The lists (one per sensor) which hold the temperature readings are pre-allocated. Also a list with labels (not shown on the graph, but anyhow mandatory) is prepared. The measurement daemon sleeps most of the time, but wakes up every 30 seconds. A lock is used when the daemon updates the temperature lists as the webserver could be reading these lists at the same time. The webserver is the most simple variant possible: regardless the clients request it always returns a page with a chart. The chart displays the last 60 temperature readings (as the list never grows beyond this number).

### Tools
I used a WiPy 2 for this project, so had to be conservative in memory usage.
Package onewire.py is copied from the Pycom documentation.
The DS18X20 works perfectly on 3.3V, but do not forget to place a 4K7 resistor between Vdd and the sensors data line. It does not matter how many sensors are connected to that data line.
Of course the WiPy must be visible in your network. See the Pycom documentation on how to setup WLAN.
