import esp32
from machine import ADC

def init_adc35():
    adc = ADC(Pin(35))        # create an ADC object acting on a pin
    valu16 = adc.read_u16()  # read a raw analog value in the range 0-65535
    valuv = adc.read_uv()   # read an analog value in microvolts
    print('Init p35 adc - raw:', valu16, 'microvolts', valuv )


def get_system_info():
    cpu_freq = machine.freq() // 1000000  # Get CPU frequency in MHz
    ram_used = gc.mem_alloc() // 1000
    ram_free = gc.mem_free() // 1000
    flash_size = esp.flash_size() // 1000
    mcu_temp = esp32.mcu_temperature() # read the internal temperature of the MCU, in Celsius
   
    
    return {
        "cpu_freq": cpu_freq,
        "cpu_temp": mcu_temp,
        "ram_used": ram_used,
        "ram_free": ram_free,
        "flash_size": flash_size
        
    }

def web_page():
    bme = bme280.BME280(i2c=i2c)
    system_info = get_system_info()
  
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

# Your existing socket setup and main loop here

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('Content = %s' % request)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        init_adc35() # init and test ADC pin 35
    except OSError as e:
        conn.close()
        print('Connection closed')
