html = b"""<!DOCTYPE html>
<html lang="en">
    <head>
        <meta http-equiv="refresh" content="5">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.3/Chart.bundle.js"></script>
        <link rel="icon" href="data:;base64,=">
        <title> WiPy </title>
    </head>
    <body>
        <div class="container" align="center">
            <div class="chart-container" style="position: relative; height:40vh; width:80vw">
                <canvas id="myChart"></canvas>
            </div>
        </div>
        <script>
            var labels = %s;
            var sensor1 = %s;
            var sensor2 = %s;
            var myChart = new Chart(document.getElementById("myChart"), {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Sensor 1',
                        borderColor: "#FF0000",
                        data: sensor1,
                        fill: false,
                        pointRadius: 1
                    }, {
                       label: 'Sensor 2',
                        borderColor: "#0000FF",
                        data: sensor2,
                        fill: false,
                        pointRadius: 1
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: 'Temperature'
                    },
                    animation: false,
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                labelString: 'Degrees Celsius',
                                display: true,
                            },
                            ticks: {
                                suggestedMin: 0,
                                suggestedMax: 70
                            }
                        }],
                        xAxes: [{
                            scaleLabel: {
                                labelString: 'Minutes',
                                display: true
                            },
                            //display: false,
                            ticks: {
                                display: false,
                                maxTicksLimit: 30
                            }
                        }]
                    }
                }
            });
        </script>
    </body>
</html>
"""

import gc
import time
import socket
import _thread
from machine import Pin
from onewire import DS18X20
from onewire import OneWire


NMEASUREMENTS = const(60)  # store this many measurements

lbl = [i for i in range(NMEASUREMENTS)]
t0 = [0.0] * NMEASUREMENTS
t1 = [0.0] * NMEASUREMENTS

t_lock = _thread.allocate_lock()


def daemon():
    global t0
    global t1
    global t_lock

    ds = DS18X20(OneWire(Pin.exp_board.G9))
    t = 0.0

    while True:
        time.sleep(27)  # measure +- every 30 seconds

        time.sleep_ms(750)
        ds.start_conversion(ds.roms[0])
        time.sleep_ms(750)
        t = ds.read_temp_async(ds.roms[0])
        with t_lock:
            t0.append(t)
            if len(t0) > NMEASUREMENTS:
                del t0[0]

        time.sleep_ms(750)
        ds.start_conversion(ds.roms[1])
        time.sleep_ms(750)
        t = ds.read_temp_async(ds.roms[1])
        with t_lock:
            t1.append(t)
            if len(t1) > NMEASUREMENTS:
                del t1[0]


_thread.start_new_thread(daemon, ())

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(socket.getaddrinfo('0.0.0.0', 80)[0][-1])
serversocket.listen(2)

while True:
    conn, addr = serversocket.accept()
    request = conn.readline()

    while True:
        line = conn.readline()
        if line == b"" or line == b"\r\n":
            break

    conn.sendall(b"HTTP/1.1 200 OK\nServer: WiPy\nContent-Type: text/html\nConnection: Closed\n\n")

    # print("request:", request)

    with t_lock:
        response = html % (lbl, t0, t1)

    conn.send(response)
    conn.sendall(b"\n")
    conn.close()

    gc.collect()
    # print(gc.mem_free())
