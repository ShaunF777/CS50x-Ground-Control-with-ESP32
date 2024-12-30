import usocket as socket
import time
from machine import Pin, SoftI2C as I2C
import machine
import network
import esp
esp.osdebug(None)

import gc
gc.collect()

import bme280

# Add a delay to prevent bootlooping
time.sleep(2)  # 2-second delay
print("Starting main program...")

# ESP32 - Pin assignment
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000)

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect('Router ssid1', 'Router password')


while station.isconnected() == False:
  pass

print('network config:', station.ipconfig('addr4'), 'SSID:', station.config('essid'))









