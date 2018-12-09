html1 = """<!DOCTYPE html>
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
        """

html2 = """
        <script>
            var labels = %s;
            var sensor1 = %s;
            var sensor2 = %s;
        </script>
        """

html3 = """
    </body>
</html>
"""

import gc
import time
import socket
import _thread
# import micropython
from machine import Pin
from onewire import DS18X20
from onewire import OneWire


NMEASUREMENTS = const(60)  # store this many measurements

lbl = [i for i in range(NMEASUREMENTS)]
t0 = [0.0] * NMEASUREMENTS
t1 = [0.0] * NMEASUREMENTS

buffer = bytearray(512)
bmview = memoryview(buffer)

t_lock = _thread.allocate_lock()


def daemon():
    """ Measure the temperature at fixed intervals """
    ds = DS18X20(OneWire(Pin.exp_board.G9))
    t = 0.0

    while True:
        # measure +- every 30 seconds
        time.sleep(27)
        for i, tx in enumerate([t0, t1]):
            time.sleep_ms(750)
            ds.start_conversion(ds.roms[i])
            time.sleep_ms(750)
            t = ds.read_temp_async(ds.roms[i])
            with t_lock:
                tx.append(t)
                if len(tx) > NMEASUREMENTS:
                    del tx[0]


_thread.start_new_thread(daemon, ())


def serve(file, conn):
    """ Send file to a connection in chuncks - lowering memory usage """
    with open(file, "rb") as fp:
        while True:
            n = fp.readinto(buffer)
            if n == 0:
                break
            conn.write(bmview[:n])


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(socket.getaddrinfo("0.0.0.0", 80)[0][-1])
serversocket.listen(1)

while True:
    conn, addr = serversocket.accept()
    request = conn.readline()

    while True:
        line = conn.readline()
        if line == b"" or line == b"\r\n":
            break

    conn.write(b"HTTP/1.1 200 OK\nServer: WiPy\nContent-Type: text/html\nConnection: Closed\n\n")

    # serve the webpage
    conn.write(html1)
    with t_lock:
        conn.write(html2 % (lbl, t0, t1))

    serve("mychart.js", conn)
    conn.write(html3)

    conn.write(b"\n")
    conn.close()

    gc.collect()
    # micropython.mem_info()
