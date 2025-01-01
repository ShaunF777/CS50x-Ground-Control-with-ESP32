# WCS1800 Current Measurement and Scaling with ADC 

This code measures current using an analog sensor (WCS1800 hall effect sensor) connected to an ESP32 microcontroller. It processes the measurements, calculates RMS (Root Mean Square) values, and interpolates scaled current values based on predefined scale points.  

## Code Breakdown  

## 1. Importing Libraries  
```python  
from machine import Pin, ADC  
from time import sleep  
import math
```
- Pin: Used to control GPIO pins on the microcontroller.
- ADC: Used for reading analog values from specified pins.
- sleep: Pauses the program for a specified duration.
- math: Provides mathematical functions, including square root calculations.
## 2. Global Variable Declaration
```py
global average_scaled_current  # Declare it as global   
average_scaled_current = 0
```
- Purpose: Initializes a global variable to store the average scaled current.
## 3. GPIO and ADC Initialization
```py
print("Initialize GPIO pins")  

pot = ADC(Pin(34))              # Initialize ADC on pin 34 for current measurement  
pot.atten(ADC.ATTN_11DB)       # Set attenuation for full range: 0 - 3.3V  

input_pin = Pin(35, Pin.IN)  
measuring_ind_pin = Pin(2, Pin.OUT)  
measuring_ind_pin.value(0)  # Default state to OFF  

print("GPIO pins initialized")
```
- Functionality:
  - Initializes the ADC on pin 34 for reading current.
  - Sets pin 35 as an input and pin 2 as an output for a measuring indicator.
  - Configures the ADC to read voltages up to 3.3V.
## 4. Constants Definition
```py
# Constants  
SENSOR_RESOLUTION = 4095  # 12-bit ADC resolution  
V_REF = 3.3  # Reference voltage of the ADC  
SCALE_FACTOR = 1 / 0.66  # Scale factor based on sensor output  
THRESHOLD = 1980  # Minimum ADC value to consider for current measurement  
SAMPLING_RATE = 0.01  # Sampling rate (100 Hz)  
SAMPLE_COUNT = 100  # Number of samples for RMS calculation
```
- Purpose: Defines constants for sensor resolution, reference voltage, scaling factors, thresholds, sampling rates, and sample counts for RMS calculations.

## 5. Scale Points for Interpolation
```py
scale_points = [  
    (2.436, 0.3),  
    (2.47, 0.84),  
    (2.48, 0.99),  
    (2.5, 1.2),  
    (2.593, 2.38),  
    (2.618, 2.84),  
    (2.7, 4.07),  
    (2.825, 5.865),  
    (2.859, 6.047),  
    (2.87, 6.36),   
    (2.95, 7.47),   
    (3.01, 8.17),   
    (3.035, 8.475),   
    (3.05, 8.730),   
    (3.085, 9.42),  
    (3.149, 10.55),  
    (3.22, 11.4),  
    (3.317, 12.8),  
    (3.38, 13.85)  
]
```
- Purpose: A list of tuples representing scale points for interpolating actual current values based on average RMS current readings.

## 6. Current Reading Function

```py
def read_current():  
    adc_value = pot.read()  # Read raw ADC value  
    voltage = (adc_value / SENSOR_RESOLUTION) * V_REF  # Convert to voltage  
    current = voltage * SCALE_FACTOR  # Convert voltage to current (A)  
    return current, adc_value  # Return current and raw ADC value
```
- Functionality: Reads the raw ADC value, converts it to voltage, and then to current, returning both values.
## 7. Interpolation Function
```py
def interpolate_scaling_factor(rms_current):  
    global last_known_scaled_current  # Use the global variable  
    scale_points.sort()  # Sort scale points  

    lower_point = None  
    upper_point = None  

    for point in scale_points:  
        if point[0] <= rms_current:  
            lower_point = point  
        elif point[0] > rms_current and upper_point is None:  
            upper_point = point  
            break  

    if lower_point and upper_point:  # Perform linear interpolation  
        slope = (upper_point[1] - lower_point[1]) / (upper_point[0] - lower_point[0])  
        last_known_scaled_current = lower_point[1] + slope * (rms_current - lower_point[0])  
        return  

    if lower_point:  # Update last known scaled current  
        last_known_scaled_current = lower_point[1]  
        return  

    return  # Do nothing if no points are found
```
- Functionality: Interpolates the scaling factor for the current based on the provided RMS current and the predefined scale points.
## 8. Main Control Loop
```python  
try:  
    while True: 
```
- Purpose: Enters an infinite loop to continuously read current values and update the measuring indicator.

### 8.1 Measuring Indicator Control
```py
    measuring_ind_pin_change_counter += 1  # Increment the counter  
    
    # Turn on the indicator every 100 iterations (2 seconds)  
    if measuring_ind_pin_change_counter >= 100:  # 100 * 0.1s = 5 seconds  
        measuring_ind_pin_value = 1  # Turn on the pump  
        measuring_ind_pin_change_counter = 0  # Reset the counter  
        
    measuring_ind_pin.value(measuring_ind_pin_value)  # Set the pin value  
    sleep(SAMPLING_RATE)  # Wait for the next sample
```
- Functionality:
Increments a counter to track the number of iterations.
Turns on the measuring indicator every 100 iterations (approximately every 5 seconds).
Sets the output pin state for the measuring indicator and sleeps for the defined sampling rate.

### 8.2 Current Reading
`current, pot_value = read_current()  # Read current and pot value`
- Functionality: Calls the read_current function to obtain the current and potentiometer value.

### 8.3 Threshold Check and RMS Calculation

```py
    if pot_value > THRESHOLD:  
        # Update max current for peak detection  
        max_current = max(max_current, current)  

        # Update the sum of squares for RMS and count the samples  
        squared_sum += current ** 2  
        sample_counter += 1  
        
        # Calculate RMS if we reached the specified sample count  
        if sample_counter >= SAMPLE_COUNT:  
            rms_current = math.sqrt(squared_sum / SAMPLE_COUNT)  # Calculate RMS  
            
            # Calculate the actual current using interpolation  
            interpolate_scaling_factor(rms_current)
```
- Functionality:
  - Checks if the potentiometer value exceeds a defined threshold.
  - Updates the maximum current detected.
  - Accumulates the square of the current for RMS calculation and increments the sample counter.
  - Calculates the RMS current when the specified number of samples is reached and interpolates the scaling factor.

### 8.4 Updating Scaled Current Samples
```py
            # Update the last scaled current samples list  
            if last_known_scaled_current is not None:  
                last_scaled_current_samples.append(last_known_scaled_current)  
                if len(last_scaled_current_samples) > 6:  
                    last_scaled_current_samples.pop(0)  # Keep only the last 6 samples  

            # Calculate the average of the last 6 scaled current readings  
            average_scaled_current = (  
                sum(last_scaled_current_samples) / len(last_scaled_current_samples)  
                if last_scaled_current_samples else 0  
            )
```
- Functionality:
Updates a list to store the last known scaled current readings, keeping only the most recent six entries.
Calculates the average of these last six scaled current readings.

### 8.5 Output Display
```py
            # Use the last known scaled current for output  
            print("Pot Value: {}, Input Pin Value: {}, Peak Current: {:.3f} A, RMS Current: {:.3f} A, Scaled Current: {:.3f} A, Average of Last 6 Scaled Currents: {:.3f} A".format(  
                pot_value, input_pin.value(), max_current, rms_current,   
                last_known_scaled_current if last_known_scaled_current is not None else 0,  
                average_scaled_current  
            ))
```
- Functionality: Prints the current values, including the potentiometer value, input pin state, peak current, RMS current, scaled current, and the average of the last six scaled currents.

### 8.6 Handling Low Potentiometer Values
```py
    else:  
        print("Ampere raw value threshold not reached, ensure connection!")  
        average_scaled_current = 0  
        print("Average of Last 6 Scaled Currents: {:.3f} A".format(  
                average_scaled_current))  
        sleep(2)
```
- Functionality: If the potentiometer value is below the threshold, it prints a warning message and resets the average scaled current.

### 8.7 Indicator Control and Sleep
```py
    # Turn off the indicator after the 100 ms sleep  
    if measuring_ind_pin_value == 1:  
        measuring_ind_pin_value = 0  # Turn off the pump after processing   
    sleep(SAMPLING_RATE)  # Wait before the next measurement
```
- Functionality: Turns off the measuring indicator after processing and waits for the next measurement based on the defined sampling rate.

### 8.8 Exception Handling
```py
except KeyboardInterrupt:  
    pass  
```
- Purpose: Allows the loop to be terminated gracefully with a keyboard interrupt (Ctrl+C).

## Summary
> 😎This code continuously measures current using an ADC sensor, calculates RMS values, and maintains an average of the last scaled current readings while controlling a measuring indicator. It handles both normal and threshold-exceeded conditions, providing feedback on the current measurement status.😎