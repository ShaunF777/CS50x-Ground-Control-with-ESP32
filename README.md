# CS50x Final Project: Ground Control with ESP32  

Build a micropython app that runs on an ESP-32, allowing scheduled control of a pump & sprinkler system. The ESP32 includes a web application with system information & adjustable schedule parameters for watering intervals.  

## Project Overview  

This project aims to:  
- Save water by disabling the sprinklers when ground moisture is sufficient.  
- Power a 0.35-2kW borehole pump that supplies water to a sprinkler system.  
- Measure pump amperage to protect the pump.  

## Diagram  

![IoT Diagram](/images/CS50x_Ground_control_IOT_diagram.jpg)  

## Parts & Functions  

- **ESP32-Wroom (Do-IT version)**: Main controller for pump monitoring and control.  
- **Relay board 3.3V**: Controls 220VAC outputs up to 10A.  
- **WCS1800 Current board 3-12V**: Measures current from 0 - 25A AC.  
- **5V DC Power Supply (PSU)**: Supplies 5V to the ESP32.  
- **Breadboard Jumpers assorted**: For connections.  
- **USB programming cable**: For programming the ESP32.  
- **AC220 Power socket with 16A plug and lead**: For power supply.  

## Possible Future Additions  

- **ESP32-C3-Mini-1**: Ground moisture & Humidity, Pressure, Temperature monitoring with bme280. Transmission of this information to the ESP32-Wroom using ESPNOW protocol.  

## Project Folders  

| Project Folder Name         | Description                                     | Readme Links                                         |  Buying the things used here       |
|-----------------------------|-------------------------------------------------|------------------------------------------------------|------------------------------------|  
| station_wroom32             | CS50x Final Project                             | [README.md](/station_wroom32/README.md)              | **Custom Built** 
| test_bme280_wroom32         | Humidity, Pressure, Temperature sensor          | [README.md](/test_bme280_wroom32/README.md)          | [BME280 with I2C](https://www.communica.co.za/products/hkd-baromtrc-sensr-bme280-3-3?variant=43731732988204)
| test_simple_io_wroom32      | Digital & analogue in & outputs                 | [README.md](/test_simple_io_wroom32/README.md)       | [ESP32-Wroom](https://www.communica.co.za/products/bmt-esp-32-wifi-b-t-dev-board)
| test_wcs1800_wroom32        | Getting RMS amps from this sensor               | [README.md](/test_wcs1800_wroom32/README.md)         | [WCS1800 Hall 25A Current Sensor](https://www.robotics.org.za/HW-671?search=wcs1800)

Each directory contains its own readme file, for a more in depth description of their code.

## Project Help and Resources 

> 💡💡💡 Before I forget, here are my sources, ladies and gentlemen. These helped me so much.

For taking notes, retention and understanding of information: 
[Notion](https://www.notion.com/)
[Sider Chatgpt Sidebar for Chrome](https://chromewebstore.google.com/detail/sider-chatgpt-sidebar-+-g/difoiogjjojoaoomphldepapgpbgkhkb)

For help getting started with different sensors and periferals even though i am using vscode:
[RandomNerdTutorials - MicroPython](https://randomnerdtutorials.com/projects-esp32-esp8266-micropython/)

## Getting started with VScode and the PyMakr extension
