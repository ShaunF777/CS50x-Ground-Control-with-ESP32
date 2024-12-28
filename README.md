CS50x Final Project: Ground Control with ASP32 
Build a micropython app that runs on an ESP-32, that allows scheduled control of a pump & sprinkler system. 
The ESP32 should include a web application with system information & adjustable schedule parameters for watering intervals.
This should allow the following:
Saving water by disabling the sprinklers when ground moisture is sufficient.
Powering a 0.35-2kw Borehole pump that supplies water to a sprinkler system.
Measuring pump amperes to protect the pump

Parts & Function:
ESP-Wroom-32 (Do-IT version) -  Main controller for Pump monitoring and control
Relay board 3.3v -              Control 220VAC outputs up to 10Amp
WCS1800 Current board 3-12v -   Measure Current 0 - 25Amp AC
5vdc Power Supply (PSU) -       Supply 5v to the ESP32
Breadboard Jumpers assorted
USB programming cable
AC220 Power socket with 16Amp plug and lead

Possible later additions to the project:
ESP32-C3-Mini-1 Ground moisture monitoring & transmittion to the ESP32-Wroom using ESPNOW protocol 