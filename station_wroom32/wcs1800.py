from machine import Pin, ADC  
from time import sleep  
import math

average_scaled_current = 0  # Declare it as global 
load_indicator = 0

print("Initialize GPIO pins")  
wcs = ADC(Pin(34))              # WCS1800 hall effect analog amperage reading   
wcs.atten(ADC.ATTN_11DB)       # Full range: 0 - 3.3V

climit_pin = Pin(35, Pin.IN)  # WCS1800 digital output can be adjusted on the board
measuring_ind_pin = Pin(12, Pin.OUT)  
measuring_ind_pin.value(0)  # Default to OFF  

print("GPIO pins initialized")  

# Constants  
SENSOR_RESOLUTION = 4095  # 12-bit ADC  
V_REF = 3.3  # Reference voltage of the ADC  
SCALE_FACTOR = 1 / 0.66  # Adjust this based on your sensor's output  
THRESHOLD = 1983  # Minimum pot value to consider for current measurement  
SAMPLING_RATE = 0.01  # Time in seconds between measurements (100 Hz)  
SAMPLE_COUNT = 100  # Number of samples for RMS calculation  

LOW_CURRENT_THRESHOLD = 0.1  # Define a low current threshold (in Amps)  
LOW_CURRENT_DURATION = 5  # Number of consecutive samples below the threshold to consider load fallen away  

# Scale points: (average RMS current, actual current measured)  
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

# Variable to store the last known scaled current  
last_known_scaled_current = None  
last_scaled_current_samples = []  # List to hold the last 6 scaled current readings  

def read_current():  
    # Read raw value from ADC  
    adc_value = wcs.read()  
    
    # Convert ADC value to voltage  
    voltage = (adc_value / SENSOR_RESOLUTION) * V_REF  
    
    # Convert voltage to current (A)  
    current = voltage * SCALE_FACTOR  
    
    return current, adc_value  # Return both current and raw ADC value  

# Function to interpolate the scaling factor based on the scale points  
def interpolate_scaling_factor(rms_current):  
    global last_known_scaled_current  # Use the global variable    

    # Sort scale points based on average RMS current  
    scale_points.sort()  

    lower_point = None  
    upper_point = None  

    for point in scale_points:  
        if point[0] <= rms_current:  
            lower_point = point  
        elif point[0] > rms_current and upper_point is None:  
            upper_point = point  
            break  

    # If both points are found, perform linear interpolation  
    if lower_point and upper_point:  
        slope = (upper_point[1] - lower_point[1]) / (upper_point[0] - lower_point[0])  
        last_known_scaled_current = lower_point[1] + slope * (rms_current - lower_point[0])  
        return  

    # If only the lower point is found, update the last known scaled current  
    if lower_point:  
        last_known_scaled_current = lower_point[1]  
        return  

    # If no points are found, do nothing (last_known_scaled_current remains unchanged)  
    return  

def get_average_scaled_current():  
    global average_scaled_current
    return average_scaled_current

def get_load_indicator():  
    global load_indicator
    return load_indicator


def monitor_current():
    global average_scaled_current  # Global needed in the function scope
    global load_indicator
    # Initialize variables for peak detection and RMS calculation  
    max_current = 0  # Peak current  
    squared_sum = 0  # Sum of squares for RMS  
    sample_counter = 0  # Count of samples taken  

    low_current_counter = 0  # Counter for consecutive low current samples  
    measuring_ind_pin_value = 0  # Initial state of the measuring pin  
    measuring_ind_pin_change_counter = 0  # Counter for measuring indicator changes 

    try:  
        while True:  
            measuring_ind_pin_change_counter += 1  # Increment the counter  
            
            # Turn on the indicator every 100 iterations (2 seconds)  
            if measuring_ind_pin_change_counter >= 100:  # 100 * 0.1s = 5 seconds  
                measuring_ind_pin_value = 1  # Turn on the pump  
                measuring_ind_pin_change_counter = 0  # Reset the counter  
                
            measuring_ind_pin.value(measuring_ind_pin_value)  # Set the pin value  
            sleep(SAMPLING_RATE)  # Wait for the next sample  
            
            current, pot_value = read_current() 
            
            # Only consider values above the threshold  
            if pot_value > THRESHOLD:  
                # Update max current for peak detection  
                max_current = max(max_current, current)  

                load_indicator = 1
                
                # Update the sum of squares for RMS and count the samples  
                squared_sum += current ** 2  
                sample_counter += 1  

                # Reset low current counter since we have valid current   
                low_current_counter = 0  
                
                # Calculate RMS if we reached the specified sample count  
                if sample_counter >= SAMPLE_COUNT:  
                    rms_current = math.sqrt(squared_sum / SAMPLE_COUNT)  # Calculate RMS  
                    
                    # Calculate the actual current using interpolation  
                    interpolate_scaling_factor(rms_current)  

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

                    # Use the last known scaled current for output  
                    print("Pot Value: {}, Input Pin Value: {}, Peak Current: {:.3f} A, RMS Current: {:.3f} A, Scaled Current: {:.3f} A, Average of Last 6 Scaled Currents: {:.3f} A".format(  
                        pot_value, climit_pin.value(), max_current, rms_current,   
                        last_known_scaled_current if last_known_scaled_current is not None else 0,  
                        average_scaled_current  
                    ))

                    # Reset for the next RMS calculation  
                    squared_sum = 0  
                    sample_counter = 0  # Reset the sample counter  

            else:  
                # Increment low current counter if current is below the threshold  
                low_current_counter += 1  

                # If the current is below the low current threshold for too long, indicate load has fallen away  
                if low_current_counter >= LOW_CURRENT_DURATION:  
                    load_indicator = 0
                    low_current_counter = 0  # Reset the low current counter 

            # Turn off the indicator after the 100 ms sleep  
            if measuring_ind_pin_value == 1:  
                measuring_ind_pin_value = 0  # Turn off the pump after processing   
            sleep(SAMPLING_RATE)  # Wait before the next measurement  
    except KeyboardInterrupt: 
        pass
