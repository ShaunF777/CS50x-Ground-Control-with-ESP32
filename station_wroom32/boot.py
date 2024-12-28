import machine
import network
import time

# Add a delay to prevent bootlooping
time.sleep(10)  # 10-second delay for reloading
print("Starting main program...")

def do_connect():  
    # Create instances for connection objects  
    station = network.WLAN(network.STA_IF)  # For ESP station to connect to a router   
    access_point = network.WLAN(network.AP_IF)  # For others to connect to the ESP Access Point  
    access_point.active(False)  # Deactivate access point interface  
    if not station.isconnected():  
        print('connecting to network...')  
        station.active(True)  
        station.connect('TP-LINK_Garage', '32HRGUM7K9FFGXLK')  
        
        # Assign static IP address
        # This line can be left out if you prefer to use DHCP 
        station.ifconfig(('10.0.0.111', '255.255.255.0', '10.0.0.254', '10.0.0.254'))  # (IP, Subnet mask, Gateway, DNS)  
        
        while not station.isconnected():  
            pass  
    print('network config:', station.ifconfig(), 'SSID:', station.config('essid'))  

do_connect()

print("Initialize GPIO pins for ESP32_WROOM")
pins_to_initialize = {
    2: 0,  # Turn off
    4: 0,  # Turn off
    5: 0,  # Turn off
    17: 1  # Turn on for test sequence
}

for pin_number, state in pins_to_initialize.items():
    pin = machine.Pin(pin_number, machine.Pin.OUT)
    pin.value(state)
print("GPIO pins initialized")







