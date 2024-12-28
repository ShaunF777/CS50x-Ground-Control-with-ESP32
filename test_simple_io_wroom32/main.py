from machine import Pin  
from time import sleep  

print("Initialize GPIO pins")  

pump_pin = Pin(5, Pin.OUT)  
aux_pin = Pin(17, Pin.OUT)  
pump_pin.value(0)  # Default to OFF  
aux_pin.value(0)   

print("GPIO pins initialized")  

# Integrate this function into your main loop  
while True:  
    pump_pin.value(0)  
    aux_pin.value(1)   
    print(f"Pin 2 (Aux): {aux_pin.value()}, Pin 5 (Pump): {pump_pin.value()}")  
    sleep(2)  

    pump_pin.value(1)  
    aux_pin.value(0)   
    print(f"Pin 2 (Aux): {aux_pin.value()}, Pin 5 (Pump): {pump_pin.value()}")  
    sleep(2)
