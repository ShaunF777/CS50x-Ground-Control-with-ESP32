import network
import time

# Add a delay to prevent bootlooping
time.sleep(2)  # 2-second delay
print("Starting main program...")

def do_connect():
 # Create instances for connection objects
    sta_if = network.WLAN(network.STA_IF) # For ESP station to connect to a router 
    ap_if = network.WLAN(network.AP_IF) # For others to connects to the ESP Access Point
    ap_if.active(False) # Deactivate accespoint interface
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Your local router SSID', 'Your routers password')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ipconfig('addr4'))

do_connect()
   
