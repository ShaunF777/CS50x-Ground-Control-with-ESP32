import machine
import network
import time

# Add a delay to prevent bootlooping
time.sleep(10)  # 10-second delay for reloading
print("Starting main program...")

# List of known networks and their passwords
KNOWN_NETWORKS = {
    'Router ssid1': 'Router password',
    'Router ssid2': 'Router password',
    'Router ssid3': 'Router password',
    'Router ssid4': 'Router password'
    }

def do_connect():  
    # Create instances for connection objects  
    station = network.WLAN(network.STA_IF)  # For ESP station to connect to a router   
    access_point = network.WLAN(network.AP_IF)  # For others to connect to the ESP Access Point  
    access_point.active(False)  # Deactivate access point interface
    
    if not station.isconnected():  
        print('Scanning for networks...')
        station.active(True)
        networks = station.scan()
        
        best_network = None
        best_rssi = -100  # Initialize with the lowest possible RSSI value
        
        for net in networks:
            ssid = net[0].decode('utf-8')
            rssi = net[3]
            if ssid in KNOWN_NETWORKS:
                print(f'Found known network: {ssid} with RSSI {rssi}')
                if rssi > best_rssi:
                    best_network = ssid
                    best_rssi = rssi
        
        if best_network:
            print(f'Connecting to the best network: {best_network}')
            station.connect(best_network, KNOWN_NETWORKS[best_network])
            
            # Assign static IP address if connecting to a specific network
            if best_network == 'TP-LINK_Garage':
                station.ifconfig(('10.0.0.111', '255.255.255.0', '10.0.0.254', '10.0.0.254'))  # (IP, Subnet mask, Gateway, DNS)
        
            while not station.isconnected():
                pass
            print('Network config:', station.ifconfig(), 'SSID:', station.config('essid'))
        else:
            print('No known networks found')
    else:
        print('Already connected to a network')
        print('Network config:', station.ifconfig(), 'SSID:', station.config('essid'))

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








