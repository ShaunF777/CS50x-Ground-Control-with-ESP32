import machine
import time
import socket
import network
import urequests
import ujson
import _thread
import ntptime

# Initialize GPIO pin for the pump
pump_pin = machine.Pin(15, machine.Pin.OUT)
pump_pin.value(0)  # Default to OFF

# Default time intervals (24-hour format)
on_hour_morning, on_minute_morning = 0, 0
off_hour_morning, off_minute_morning = 0, 0
on_hour_afternoon, on_minute_afternoon = 0, 0
off_hour_afternoon, off_minute_afternoon = 0, 0

# HTML template with a toggle button and forms
html = """<!DOCTYPE html>
<html>
    <head> 
        <title>ESP32 Pump Control</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
            form { margin-bottom: 20px; }
            label, input { display: block; margin-bottom: 5px; }
            input[type="submit"] { margin-top: 10px; }
        </style>
        <script>
            function togglePump() {
                fetch('/toggle')
                    .then(response => response.text())
                    .then(data => {
                        document.getElementById('pumpStatus').innerText = data;
                    });
            }
            
            function updateSettings() {
                fetch('/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams(new FormData(document.getElementById('settingsForm')))
                })
                .then(response => response.text())
                .then(data => {
                    document.getElementById('settingsStatus').innerText = data;
                });
            }

            function fetchTime() {
                fetch('/time')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('currentTime').innerText = `Current Time: ${data.time}`;
                    });
            }
            
            setInterval(fetchTime, 10000); // Update time every 10 seconds
            window.onload = fetchTime;
        </script>
    </head>
    <body> 
        <h1>ESP32 Pump Control</h1>
        <button onclick="togglePump()">Toggle Pump</button>
        <p id="pumpStatus">Pump is OFF</p>
        <p id="currentTime">Current Time: Loading...</p>
        <form id="settingsForm" onsubmit="event.preventDefault(); updateSettings();">
            <h2>Set Morning Intervals</h2>
            <label>ON Hour:</label>
            <input type="number" name="on_hour_morning" value="0" min="0" max="23">
            <label>ON Minute:</label>
            <input type="number" name="on_minute_morning" value="0" min="0" max="59">
            <label>OFF Hour:</label>
            <input type="number" name="off_hour_morning" value="0" min="0" max="23">
            <label>OFF Minute:</label>
            <input type="number" name="off_minute_morning" value="0" min="0" max="59">
            
            <h2>Set Afternoon Intervals</h2>
            <label>ON Hour:</label>
            <input type="number" name="on_hour_afternoon" value="0" min="0" max="23">
            <label>ON Minute:</label>
            <input type="number" name="on_minute_afternoon" value="0" min="0" max="59">
            <label>OFF Hour:</label>
            <input type="number" name="off_hour_afternoon" value="0" min="0" max="23">
            <label>OFF Minute:</label>
            <input type="number" name="off_minute_afternoon" value="0" min="0" max="59">
            <input type="submit" value="Update Settings">
        </form>
        <p id="settingsStatus">Settings are updated.</p>
    </body>
</html>
"""

# Global timezone offset in seconds (UTC+2 for Johannesburg)
TIMEZONE_OFFSET = 2 * 3600

# Sync time with NTP and adjust for Johannesburg (UTC+2)
def sync_time_periodically():
    global TIMEZONE_OFFSET
    while True:
        ntptime.settime()  # Sync the RTC to UTC
        print("Time synchronized with NTP")
        time.sleep(3600)  # Sync every hour

_thread.start_new_thread(sync_time_periodically, ())

# Custom wrapper for local time with timezone adjustment
def get_adjusted_localtime():
    t = time.localtime(time.time() + TIMEZONE_OFFSET)  # Apply timezone offset
    return t

# Replace get_current_time with RTC time
def get_current_time():
    current_time = get_adjusted_localtime()  # Use adjusted time 
    return f"{current_time[0]}-{current_time[1]:02d}-{current_time[2]:02d} {current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}"

def handle_root(client):
    response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + html
    client.send(response.encode())

def handle_toggle(client):
    global pump_pin
    pump_pin.value(not pump_pin.value())  # Toggle the pump state
    status = 'Pump is ON' if pump_pin.value() else 'Pump is OFF'
    response = 'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n' + status
    client.send(response.encode())

def handle_update(client, request_body):
    global on_hour_morning, on_minute_morning, off_hour_morning, off_minute_morning
    global on_hour_afternoon, on_minute_afternoon, off_hour_afternoon, off_minute_afternoon
    
    params = dict(x.split('=') for x in request_body.split('&'))
    on_hour_morning = int(params.get('on_hour_morning', '0'))
    on_minute_morning = int(params.get('on_minute_morning', '0'))
    off_hour_morning = int(params.get('off_hour_morning', '0'))
    off_minute_morning = int(params.get('off_minute_morning', '0'))
    on_hour_afternoon = int(params.get('on_hour_afternoon', '0'))
    on_minute_afternoon = int(params.get('on_minute_afternoon', '0'))
    off_hour_afternoon = int(params.get('off_hour_afternoon', '0'))
    off_minute_afternoon = int(params.get('off_minute_afternoon', '0'))
    
    response = 'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\nSettings updated successfully.'
    client.send(response.encode())

def handle_time(client):
    current_time = get_current_time()
    if current_time:
        response = {'time': current_time}
        client.send('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n' + ujson.dumps(response))
    else:
        client.send('HTTP/1.0 500 Internal Server Error\r\n\r\n'.encode())

# Function to check and activate/deactivate pump based on time intervals
def time_based_control():
    while True:
        current_time = get_current_time()
        if current_time:
            current_hour = int(current_time[11:13])
            current_minute = int(current_time[14:16])
            print(f"Current Time: {current_hour}:{current_minute}")  # 🟣 Debugging current time
            print(f"Morning ON: {on_hour_morning}:{on_minute_morning}, OFF: {off_hour_morning}:{off_minute_morning}")  # 🟣 Debugging intervals
            print(f"Afternoon ON: {on_hour_afternoon}:{on_minute_afternoon}, OFF: {off_hour_afternoon}:{off_minute_afternoon}")  # 🟣 Debugging intervals
            
            # Morning interval check
            if (current_hour == on_hour_morning and current_minute == on_minute_morning):
                if pump_pin.value() == 0:  # Only turn on if the pump is currently off
                    pump_pin.value(1)
                    print("Pump turned ON for morning session")  # 🟣 Debugging message
            elif (current_hour == off_hour_morning and current_minute == off_minute_morning):
                if pump_pin.value() == 1:  # Only turn off if the pump is currently on
                    pump_pin.value(0)
                    print("Pump turned OFF for morning session")  # 🟣 Debugging message
            
            # Afternoon interval check
            if (current_hour == on_hour_afternoon and current_minute == on_minute_afternoon):
                if pump_pin.value() == 0:   # Only turn on if the pump is currently off
                    pump_pin.value(1)
                    print("Pump turned ON for afternoon session")  # 🟣 Debugging message
            elif (current_hour == off_hour_afternoon and current_minute == off_minute_afternoon):
                if pump_pin.value() == 1:   # Only turn off if the pump is currently on
                    pump_pin.value(0)
                    print("Pump turned OFF for afternoon session")  # 🟣 Debugging message

        time.sleep(30)  # Check every 30 seconds

# Start the time-based control in a separate thread
_thread.start_new_thread(time_based_control, ())

# Bind the socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

while True:
    # Accept a new client connection
    cl, addr = s.accept()
    print('client connected from', addr)

    # Read the client's request
    request = cl.recv(1024).decode()
    request_line = request.split('\r\n')[0]
    method, path, _ = request_line.split()

    if path == '/':
        handle_root(cl)
    elif path == '/toggle':
        handle_toggle(cl)
    elif path == '/update' and method == 'POST':
        request_body = request.split('\r\n')[-1]
        handle_update(cl, request_body)
    elif path == '/time':
        handle_time(cl)

    cl.close()
