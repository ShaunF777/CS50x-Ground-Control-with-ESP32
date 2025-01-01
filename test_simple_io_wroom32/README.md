# GPIO Control for Pump and Auxiliary Device  

This code initializes two GPIO pins on a microcontroller (likely an ESP32 or similar) to control a pump and an auxiliary device. It alternates the states of these pins in a loop.  

## Code Breakdown  

### 1. Importing Libraries  
```python  
from machine import Pin  
from time import sleep
```

- Pin: Used to control GPIO pins on the microcontroller.
- sleep: Allows the program to pause for a specified amount of time.

## Initialization

```py
print("Initialize GPIO pins")  

pump_pin = Pin(5, Pin.OUT)  # Initialize pin 5 as an output for the pump  
aux_pin = Pin(17, Pin.OUT)   # Initialize pin 17 as an output for the auxiliary device  
pump_pin.value(0)            # Set the pump pin to OFF (0)  
aux_pin.value(0)             # Set the auxiliary pin to OFF (0)  

print("GPIO pins initialized")
```
- Functionality:
  - Initializes GPIO pin 5 for the pump and pin 17 for the auxiliary device as output pins.
  - Sets both pins to a low state (OFF) initially.

## Main Control Loop
```py
while True:  
    pump_pin.value(0)        # Turn OFF the pump  
    aux_pin.value(1)         # Turn ON the auxiliary device  
    print(f"Pin 2 (Aux): {aux_pin.value()}, Pin 5 (Pump): {pump_pin.value()}")  
    sleep(2)                 # Wait for 2 seconds  

    pump_pin.value(1)        # Turn ON the pump  
    aux_pin.value(0)         # Turn OFF the auxiliary device  
    print(f"Pin 2 (Aux): {aux_pin.value()}, Pin 5 (Pump): {pump_pin.value()}")  
    sleep(2)                 # Wait for 2 seconds
```
- Functionality:Enters an infinite loop where it alternates the states of the pump and auxiliary pins:
  - First, it turns the pump OFF and the auxiliary device ON, printing their states and pausing for 2 seconds.
  - Then, it turns the pump ON and the auxiliary device OFF, again printing their states and pausing for another 2 seconds.

> 😋This code continuously toggles the state of a pump and an auxiliary device connected to GPIO pins on a microcontroller. It provides a simple mechanism to control these devices in an alternating manner, with a 2-second delay between state changes.😋