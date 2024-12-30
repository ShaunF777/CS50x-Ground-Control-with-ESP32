# CS50x Final Project: Ground Control with ESP32
## Introduction  
> 🐱 **WELCOME!!!** 🐱 to my 1st full repo. This readme will share an overview of requirements to build my project the same way i did. Using a windows PC, VScode, PyMakr extention & programming in [Micropython](https://micropython.org/).
Build a micropython app that runs on an ESP-32, allowing scheduled control of a pump & sprinkler system. In short, the python code includes the front end HTML,CSS & JavaScript, as well as all the backend, connection, monitoring & serving code. Small but perfect for any person persuing full-stack dev. The ESP32 hosts this web application, serving the client with system information & forms for changing scheduled parameters for watering intervals. 

> ☄️ **PS:_VERY_IMPORTANT_NOTICE:** ☄️ Compiling & Loading C++ to the esp32 takes 20x time. In `retrospect` i wasted many hours, because I many times doubted the capabilities of the ESP32 and the micropython running on it & then each time went back to C/C++ Arduino and even Espressif-IDE frameworks. But then seeing how long it takes to compile and load, i just went back to [Micropython](https://micropython.org/). Dont do this to yourself, read my tips and pointers below in [Get started with VScode PyMakr extension](#get-started-with-vscode-pymakr-extension)  

## Table of Contents 
- [Introduction](#introduction) 
- [Project Usage](#project-usage) 
- [Diagram](#diagram) 
- [Parts & Functions](#parts-and-functions) 
- [Future Additions](#future-additions) 
- [Project Folders](#project-folders)
- [Project Help & Resources](#project-help-and-resources)
- [Get started with VScode PyMakr extension](#get-started-with-vscode-pymakr-extension)

## Project Usage

This project aims to:  
- Save water by disabling the sprinklers when ground moisture is sufficient.  
- Power a 0.35-2kW borehole pump that supplies water to a sprinkler system.  
- Measure pump amperage to protect the pump.  

## Diagram  

![IoT Diagram](/images/CS50x_Ground_control_IOT_diagram.jpg)  

## Parts and Functions

- **ESP32-Wroom (Do-IT version)**: Main controller for pump monitoring and control.  
- **Relay board 3.3V**: Controls 220VAC outputs up to 10A.  
- **WCS1800 Current board 3-12V**: Measures current from 0 - 25A AC.  
- **5V DC Power Supply (PSU)**: Supplies 5V to the ESP32.  
- **Breadboard Jumpers assorted**: For connections.  
- **USB programming cable**: For programming the ESP32.  
- **AC220 Power socket with 16A plug and lead**: For power supply.  

## Future Additions  

- **ESP32-Wroom**: Calculating total Kwh, and posting the information to a cloud service, for better graphic histograms or trends.   

- **ESP32-C3-Mini-1**: Remote Soil moisture & Humidity, Pressure, Temperature monitoring with bme280. Transmission of this information to the ESP32-Wroom using ESPNOW protocol.  

## Project Folders  

| Project Folder Name         | Description                                     | Readme Links                                         |  Buying the things used here       |
|-----------------------------|-------------------------------------------------|------------------------------------------------------|------------------------------------|  
| station_wroom32             | CS50x Final Project                             | [README.md](/station_wroom32/README.md)              | [3,3V 2 Channel High/Low Level Triger Relay Module with Optocoupler](https://www.communica.co.za/products/bdd-relay-board-2ch-3-3v?utm_source=www.communica.co.za&variant=47620050616620&sfdr_ptcid=31591_617_701056022&sfdr_hash=99be365224499160d9bb1f33df9e1613&gad_source=1&gclid=Cj0KCQiA4L67BhDUARIsADWrl7ESoeNl58OGLH5leLPfqXxXJ2_CKvnr-xlaqCA4ljWwufKBiJU78XAaAkmbEALw_wcB) 
| test_bme280_wroom32         | Humidity, Pressure, Temperature sensor          | [README.md](/test_bme280_wroom32/README.md)          | [BME280 with I2C](https://www.communica.co.za/products/hkd-baromtrc-sensr-bme280-3-3?variant=43731732988204)
| test_simple_io_wroom32      | Digital & analogue in & outputs                 | [README.md](/test_simple_io_wroom32/README.md)       | [ESP32-Wroom](https://www.communica.co.za/products/bmt-esp-32-wifi-b-t-dev-board)
| test_wcs1800_wroom32        | Getting RMS amps from this sensor               | [README.md](/test_wcs1800_wroom32/README.md)         | [WCS1800 Hall 25A Current Sensor](https://www.robotics.org.za/HW-671?search=wcs1800)

Each directory contains its own readme file, for a more in depth description of their code.

## Project Help and Resources 

> 💡💡💡 Before I forget, here are my sources, ladies and gentlemen. These helped me so much.

For taking notes, retention and understanding of information: 
[Notion](https://www.notion.com/), 
[Sider - Chatgpt Sidebar for Chrome](https://chromewebstore.google.com/detail/sider-chatgpt-sidebar-+-g/difoiogjjojoaoomphldepapgpbgkhkb)

For help getting started with different sensors and periferals even though i am using vscode:
[RandomNerdTutorials - MicroPython](https://randomnerdtutorials.com/projects-esp32-esp8266-micropython/)

## Get started with VScode PyMakr extension
