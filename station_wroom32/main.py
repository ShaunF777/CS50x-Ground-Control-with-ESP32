import usocket as socket
import time
import machine
import _thread
import uos  # Import uos for file handling
from timesync import get_current_time # from timesync.py
from timesync import sync_time_periodically # from timesync.py
from wcs1800 import monitor_current, get_load_indicator, get_average_scaled_current # from wcs.py the function
import esp
esp.osdebug(None)

import gc
gc.collect()

time.sleep(2)
# Initialize GPIO pin for the pump
pump_pin = machine.Pin(5, machine.Pin.OUT)
pump_pin.value(0)  # Default to OFF

# Initialize GPIO pin 17 for extra
aux_pin = machine.Pin(17, machine.Pin.OUT)
aux_pin.value(0)  # Default to OFF

# File to store the activation times
TIME_FILE = "pump_times.txt"

# Read pump times from the file
def read_pump_times_amps():
    global min_amp, max_amp, on_hour, on_minute, off_hour, off_minute
    try:
        with open(TIME_FILE, "r") as f:
            data = f.read().split(",")
            min_amp = int(data[0])
            max_amp = int(data[1])
            on_hour = int(data[2])
            on_minute = int(data[3])
            off_hour = int(data[4])
            off_minute = int(data[5])
    except (OSError, ValueError):
        # Default values if the file doesn't exist or the data is corrupted
        min_amp, max_amp = 1, 9  # Default Amps
        on_hour, on_minute = 16, 30  # Default pump ON time
        off_hour, off_minute = 19, 0  # Default pump OFF time

# Write pump times and amps to the file
def write_pump_times_amps():
    try:
        with open(TIME_FILE, "w") as f:
            f.write(f"{min_amp},{max_amp},{on_hour},{on_minute},{off_hour},{off_minute}")
    except OSError as e:
        print("Error writing/saving pump parameters:", e)

# Read the saved pump times at startup
read_pump_times_amps()

def get_system_info():
    ram_used = gc.mem_alloc() // 1000
    ram_free = gc.mem_free() // 1000
    
    return {
        "ram_used": ram_used,
        "ram_free": ram_free,
    }

def web_page(load_status, av_current_drawn, satime, min_amp, max_amp, on_hour, on_minute, off_hour, off_minute, pump_pin, aux_pin, status_message=''):
    system_info = get_system_info()
  
    html = f"""
    <html>
        <head>
            <title>ESP32</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <meta http-equiv="refresh" content="20">
            <style> 
                body {{ text-align: center; font-family: "Trebuchet MS", Arial; margin: 0; padding: 20px;
                    background-color:rgb(164, 16, 52);}}
                table {{ border-collapse: collapse; width: 50%; margin-left: auto; margin-right: auto; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; }}
                th {{ background-color: #0043af; color: white; }}
                tr:hover {{ background-color: #f2f2f2; }}
                .sensor {{ color: black; font-weight: bold; }}
                .info {{ color: black; font-weight: bold; }}
                .status-message {{  
                    color: red;  
                    font-size: 1.5em; /* Equivalent to H2 size */ }} 
            </style>
        </head>
        <body>
            <h1>CS50x Ground Control with ESP32</h1>
            <table>
                <tr><th>MEASUREMENT</th><th>VALUE</th></tr>
                <tr><td>South African Time</td><td><span class="info">{satime}</span></td></tr>
                <tr><td>RAM Used</td><td><span class="info">{system_info['ram_used']} Kb</span></td></tr>
                <tr><td>RAM Free</td><td><span class="info">{system_info['ram_free']} Kb</span></td></tr>
                <tr><td>Last Known Average Current</td><td><span class="info">{av_current_drawn} Amp</span></td></tr>
                <tr><td>Load Connected</td><td><span class="info">{load_status} </span></td></tr>
                <tr><td>GPIO 5 Status</td><td><span class="info">{pump_pin.value()} </span></td></tr>
                <tr><td>GPIO 17 Status</td><td><span class="info">{aux_pin.value()} </span></td></tr>
            </table>
            <p class="status-message">{status_message}</p>  <!-- Display status message here --> 
            <h2>Set Pump Activation Times</h2>
            <form action="/update" method="post">
                <label>ON Hour:</label>
                <input type="number" name="on_hour" value="{on_hour}" min="0" max="23">
                <label>ON Minute:</label>
                <input type="number" name="on_minute" value="{on_minute}" min="0" max="59">
                <br>
                <label>OFF Hour:</label>
                <input type="number" name="off_hour" value="{off_hour}" min="0" max="23">
                <label>OFF Minute:</label>
                <input type="number" name="off_minute" value="{off_minute}" min="0" max="59">
                <h2>Set Pump Min/Max Current Shut-off</h2>
                <label>Minimum Amps (0-12):</label>
                <input type="number" name="min_amp" value="{min_amp}" min="0" max="12">
                <br>
                <label>Maximum Amps (2-13):</label>
                <input type="number" name="max_amp" value="{max_amp}" min="2" max="13">
                <br>
                <input type="submit" value="Update Settings">
            </form>
            <h2>Toggle Control Outputs</h2>  
            <form action="/toggle" method="post">  
                <button type="submit" name="pin" value="5">Toggle Pin 5</button>  
                <button type="submit" name="pin" value="17">Toggle Pin 17</button>  
            </form> 
        </body>
    </html>
    """
    return html

def time_based_control():
    global on_hour, on_minute, off_hour, off_minute
    while True:
        current_time = get_current_time()
        time.sleep(5)
        if current_time:
            current_hour = int(current_time[11:13])
            current_minute = int(current_time[14:16])
            print(f"Current Time: {current_hour}:{current_minute}")  # Debugging current time
            print(f"Session ON: {on_hour}:{on_minute}, OFF: {off_hour}:{off_minute}")  # Debugging intervals
            
            # Check for pump activation and deactivation based on time intervals
            if (current_hour == on_hour and current_minute == on_minute):
                if pump_pin.value() == 0:  # Only turn on if the pump is currently off
                    pump_pin.value(1)
                    print("Pump turned ON")  # Debugging message
            elif (current_hour == off_hour and current_minute == off_minute):
                if pump_pin.value() == 1:  # Only turn off if the pump is currently on
                    pump_pin.value(0)
                    print("Pump turned OFF")  # Debugging message
            
        time.sleep(10)  # Check every 10 seconds

# Start the time-based control in a separate thread
_thread.start_new_thread(time_based_control, ())

def amps_based_control():
    global pump_pin, av_current_drawn, min_amp, max_amp
    while True:
        if pump_pin.value():
            time.sleep(10) # time before amp limits will be tested

            if av_current_drawn > max_amp:
                if pump_pin.value() == 1:  # Only turn off if the pump is currently on
                    pump_pin.value(0)
                    print("Over amp! Pump turned OFF")  # Debugging message
            if av_current_drawn < min_amp:
                if pump_pin.value() == 1:  # Only turn off if the pump is currently on
                    pump_pin.value(0)
                    print("Under amp! Pump turned OFF")  # Debugging message


# Start the amps_based_control in a separate thread
_thread.start_new_thread(amps_based_control, ())

# Start the monitor_current in a separate thread
_thread.start_new_thread(monitor_current, ())

# Start the sync_time_periodically in a separate thread
_thread.start_new_thread(sync_time_periodically, ())

print("Initializing socket setup")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print("Web server is listening on port 80...")

while True:
    satime = get_current_time()
    status_message = ""
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = request.decode()
        print('Content = %s' % request)

        av_current_drawn = round(get_average_scaled_current(), 2)  # Round average current drawn to 2 decimals 
        print(f"Average Current Drawn: {av_current_drawn}")
        load = get_load_indicator()
        load_status = "Connected" if load else "Disconnected"  # Determine load status 

        # Handle the form submission for updating settings  
        if 'POST' in request:  
            # Extract the request body  
            request_body = request.split('\r\n\r\n')[1] if '\r\n\r\n' in request else ''  
            print(f"Request Body: {request_body}")  # Debugging line to check the request body  
            
            # Parse the request body manually  
            params = {}  
            if request_body:  
                pairs = request_body.split('&')  
                for pair in pairs:  
                    if '=' in pair:  
                        key, value = pair.split('=', 1)  # Split only on the first '='  
                        params[key] = value  
            
            print(f"Parsed Parameters: {params}")  # Debugging line to check parsed parameters  
            
            if "/update" in request:  # Update settings request  
                min_amp = int(params.get('min_amp', '3'))  # Use '3' as default if not found  
                max_amp = int(params.get('max_amp', '7'))  # Use '7' as default if not found  
                on_hour = int(params.get('on_hour', '8'))  # Use '8' as default if not found  
                on_minute = int(params.get('on_minute', '30'))  # Use '30' as default if not found  
                off_hour = int(params.get('off_hour', '9'))  # Use '9' as default if not found  
                off_minute = int(params.get('off_minute', '0'))  # Use '0' as default if not found  
                print(f"Updated ON Time: {on_hour}:{on_minute}, OFF Time: {off_hour}:{off_minute}")  
                print(f"Updated Min amps: {min_amp}, Max amps: {max_amp}")  
                
                # Save the updated times to the file  
                write_pump_times_amps() 
                status_message = "Settings updated successfully!"  

            elif "/toggle" in request:  # Handle toggle button press  
                pin_to_toggle = int(params.get('pin', '5'))  # Default to pin 5 if not specified  
                
                if pin_to_toggle in [5, 17]:  
                    # Toggle the specified pin  
                    pin = machine.Pin(pin_to_toggle, machine.Pin.OUT)  
                    pin.value(1 - pin.value())  # Toggle the pin state (1 -> 0 or 0 -> 1)  
                    print(f"Toggled Pin {pin_to_toggle} to {pin.value()}")  # Debugging message
                    status_message = f"Pin {pin_to_toggle} toggled successfully!" 

        # Render the web page with updated status
        response = web_page(load_status, av_current_drawn, satime, min_amp, max_amp, on_hour, on_minute, off_hour, off_minute, pump_pin, aux_pin, status_message)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response.encode())
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
