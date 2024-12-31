# Using the BME280 

Build a micropython app that runs on an ESP-32, allowing scheduled control of a pump & sprinkler system. The ESP32 includes a web application with system information & adjustable schedule parameters for watering intervals.  

## Project Overview  

This project aims to:  
- Save water by disabling the sprinklers when ground moisture is sufficient.  
- Power a 0.35-2kW borehole pump that supplies water to a sprinkler system.  
- Measure pump amperage to protect the pump.  

## Diagram  

![IoT Diagram](CS50x_Ground_control_IOT_diagram.jpg)  

## Parts & Functions  

- **ESP-Wroom-32 (Do-IT version)**: Main controller for pump monitoring and control.  
- **Relay board 3.3V**: Controls 220VAC outputs up to 10A.  
- **WCS1800 Current board 3-12V**: Measures current from 0 - 25A AC.  
- **5V DC Power Supply (PSU)**: Supplies 5V to the ESP32.  
- **Breadboard Jumpers assorted**: For connections.  
- **USB programming cable**: For programming the ESP32.  
- **AC220 Power socket with 16A plug and lead**: For power supply.  

## Possible Future Additions  

- **ESP32-C3-Mini-1**: Ground moisture monitoring and transmission to the ESP32-Wroom using ESPNOW protocol.  

## Project Folders  

| Project Folder      | Description                                     | Hardware Links         |  
|---------------------|-------------------------------------------------|-------------------------|  
| station_wroom32            | Description of Folder 1                         | [Link to Hardware 1](#) |  
| test_bme280_wroom32            | Description of Folder 2                         | [Link to Hardware 2](#) |  
| test_simple_io_wroom32            | Description of Folder 3                         | [Link to Hardware 3](#) |  
| test_wcs1800_wroom32            | Description of Folder 4                         | [Link to Hardware 4](#) |  

Each directory contains its own readme file, for a more in depth description of the code they contain.

## Project Help and Resources 
Before i forget, here are my sources, ladies and gentleme, these helped me so much

For taking notes, retention and understanding of information: 
[Notion](https://www.notion.com/)
[Sider Chatgpt Sidebar for Chrome](https://chromewebstore.google.com/detail/sider-chatgpt-sidebar-+-g/difoiogjjojoaoomphldepapgpbgkhkb)

For help getting started with different sensors and periferals even though i am using vscode:
[RandomNerdTutorials - MicroPython](https://randomnerdtutorials.com/projects-esp32-esp8266-micropython/)
