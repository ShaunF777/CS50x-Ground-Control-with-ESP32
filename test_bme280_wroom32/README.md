# ESP32 Web Server with Sensor Readings from BME280  

This code sets up a web server on an ESP32 microcontroller that reads data from a BME280 sensor and displays system information. It also initializes an ADC (Analog-to-Digital Converter) on pin 35.  

## Code Breakdown  

### 1. Importing Libraries  
```py  
import esp32  
from machine import ADC
```
- esp32: Provides functions to interact with the ESP32 hardware.
- ADC: Used to read analog values from specified pins.

## ADC Initialization Function

```py
def init_adc35():  
    adc = ADC(Pin(35))        # create an ADC object acting on pin 35  
    valu16 = adc.read_u16()   # read a raw analog value (0-65535)  
    valuv = adc.read_uv()     # read an analog value in microvolts  
    print('Init p35 adc - raw:', valu16, 'microvolts', valuv)
```
- Function Purpose: Initializes the ADC on pin 35, reads a raw analog value and its corresponding voltage in microvolts, and prints the results.

## System Information Retrieval Function

```py
def get_system_info():  
    cpu_freq = machine.freq() // 1000000  # Get CPU frequency in MHz  
    ram_used = gc.mem_alloc() // 1000      # Memory allocated (used)  
    ram_free = gc.mem_free() // 1000       # Free memory  
    flash_size = esp.flash_size() // 1000  # Flash size in KB  
    mcu_temp = esp32.mcu_temperature()      # Read internal MCU temperature in Celsius  

    return {  
        "cpu_freq": cpu_freq,  
        "cpu_temp": mcu_temp,  
        "ram_used": ram_used,  
        "ram_free": ram_free,  
        "flash_size": flash_size  
    }
```
- Function Purpose: Gathers and returns key system information including CPU frequency, RAM usage, flash size, and MCU temperature.

## HTML Web Page Generation Function

```html
def web_page():  
    bme = bme280.BME280(i2c=i2c)  # Initialize BME280 sensor  
    system_info = get_system_info()  # Retrieve system information  

    html = f"""  
    <html>  
        <head>  
            <title>ESP32 Temp, Pressure, Humidity</title>  
            <meta name="viewport" content="width=device-width, initial-scale=1">  
            <meta http-equiv="refresh" content="10">  
            <style>   
                body {{ text-align: center; font-family: "Trebuchet MS", Arial; margin: 0; padding: 20px; }}  
                table {{ border-collapse: collapse; width: 50%; margin-left: auto; margin-right: auto; }}  
                th, td {{ padding: 12px; border: 1px solid #ddd; }}  
                th {{ background-color: #0043af; color: white; }}  
                tr:hover {{ background-color: #f2f2f2; }}  
                .sensor {{ color: black; font-weight: bold; }}  
                .info {{ color: black; font-weight: bold; }}  
            </style>  
        </head>  
        <body>  
            <h1>ESP32 with BME280</h1>  
            <table>  
                <tr><th>MEASUREMENT</th><th>VALUE</th></tr>  
                <tr><td>Temp. Celsius</td><td><span class="sensor">{bme.temperatureC}</span></td></tr>  
                <tr><td>Temp. Fahrenheit</td><td><span class="sensor">{bme.temperatureF}</span></td></tr>  
                <tr><td>Pressure</td><td><span class="sensor">{bme.pressure}</span></td></tr>  
                <tr><td>Humidity</td><td><span class="sensor">{bme.humidity}</span></td></tr>  
            </table>  
            <h1>ESP32 System Information</h1>  
            <table>  
                <tr><th>MEASUREMENT</th><th>VALUE</th></tr>  
                <tr><td>CPU Frequency</td><td><span class="info">{system_info['cpu_freq']} MHz</span></td></tr>  
                <tr><td>CPU Temperature</td><td><span class="info">{system_info['cpu_temp']} C</span></td></tr>  
                <tr><td>RAM Used</td><td><span class="info">{system_info['ram_used']} Kb</span></td></tr>  
                <tr><td>RAM Free</td><td><span class="info">{system_info['ram_free']} Kb</span></td></tr>  
                <tr><td>Flash Size</td><td><span class="info">{system_info['flash_size']} Kb</span></td></tr>  
            </table>  
        </body>  
    </html>  
    """  
    return html
```
- Function Purpose: Generates an HTML page displaying temperature, pressure, humidity readings from the BME280 sensor along with system information.

## Socket Setup and Main Loop
```py
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind(('', 80))  
s.listen(5)  

while True:  
    try:  
        if gc.mem_free() < 102000:  
            gc.collect()  # Garbage collect if free memory is low  
        conn, addr = s.accept()  # Accept a new connection  
        conn.settimeout(3.0)  
        print('Got a connection from %s' % str(addr))  
        request = conn.recv(1024)  
        conn.settimeout(None)  
        request = str(request)  
        print('Content = %s' % request)  
        response = web_page()  # Generate the web page  
        conn.send('HTTP/1.1 200 OK\n')  
        conn.send('Content-Type: text/html\n')  
        conn.send('Connection: close\n\n')  
        conn.sendall(response)  # Send the web page to the client  
        conn.close()  
        init_adc35()  # Initialize and test ADC pin 35  
    except OSError as e:  
        conn.close()  
        print('Connection closed')
```
- Functionality:
  - Sets up a TCP socket on port 80 to listen for incoming connections.
  - Accepts connections and serves the generated HTML page containing sensor and system information.
  - Calls init_adc35() to test the ADC on pin 35 after each connection.

## Summary
> 😄This code provides a simple web interface to monitor environmental conditions (temperature, pressure, humidity) and system status (CPU frequency, temperature, RAM usage, flash size) of an ESP32 device, while also demonstrating the use of an ADC.😄

