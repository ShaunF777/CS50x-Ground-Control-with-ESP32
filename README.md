# CS50x Final Project: Ground Control with ESP32
## Introduction  
> 🐱 **WELCOME!!!** 🐱 to my 1st full repo. This readme will share an overview of requirements to build my project the same way i did. Using a windows PC, [VScode](https://code.visualstudio.com/download), [PyMakr](https://github.com/sg-wireless/pymakr-vsc) extention & programming in [Micropython](https://micropython.org/).
Build a micropython app that runs on an ESP-32, allowing scheduled control of a pump & sprinkler system. In short, the python code includes the front end HTML,CSS & JavaScript, as well as all the backend, connection, monitoring & serving code. Small but perfect for any person persuing full-stack dev. The ESP32 hosts this web application, serving the client with system information & forms for changing scheduled parameters for watering intervals. 

> ☄️ **PS:_VERY_IMPORTANT_NOTICE:** ☄️ Compiling & Loading C++ to the esp32 takes 10-20x times longer. In `retrospect` i wasted many hours because I sometimes doubted the capabilities of the ESP32 and the micropython running on it & then each time went back to C/C++ Arduino and even Espressif-IDE frameworks. But then seeing how long it takes to compile and load, i just went back to [Micropython](https://micropython.org/). Dont do this to yourself, read my tips and pointers below in [Get started with VScode PyMakr extension](#get-started-with-vscode-pymakr-extension)  

## Table of Contents 
- [Introduction](#introduction) 
- [Project Usage](#project-usage) 
- [Diagram](#diagram) 
- [Parts & Functions](#parts-and-functions) 
- [Future Additions](#future-additions) 
- [Project Folders](#project-folders)
- [Project Help & Resources](#project-help-and-resources)
- [Program Flow Summary](#program-flow-summary) 
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

## Program Flow Summary
### 1 bootpy Execution

- The boot.py file runs once when the ESP32 is powered on or reset. It initializes essential tasks such as establishing a Wi-Fi connection and setting up initial GPIO configurations. This file ensures that the ESP32 is ready for operation before running the main program.

### 2. Importing Modules:

**The main.py file starts by importing necessary modules, including usocket, machine, and _thread, as well as custom functions from timesync.py and wcs1800.py.**
- From timesync.py, it imports get_current_time for retrieving the current time and sync_time_periodically for periodic time synchronization.
- From wcs1800.py, it imports monitor_current, get_load_indicator, and get_average_scaled_current for handling current monitoring and load detection.
### 3. Initialization:

- The program initializes GPIO pins for the pump and an auxiliary device, setting their default states to OFF. It also prepares a file (pump_times.txt) to store pump activation times and current limits.
- The function read_pump_times_amps() is called to read the saved activation times and current limits from the file. If the file is missing or corrupt, default values are assigned.

### 4. Web Server Setup:

A socket is created to listen for incoming HTTP requests on port 80. This sets up a simple web server, allowing users to interact with the ESP32 through a web interface.

### 5. Threaded Functions:

**Several critical functions are started in separate threads to run concurrently:**
- **`time_based_control():`** Monitors the current time and activates or deactivates the pump based on predefined ON and OFF times.
- **`amps_based_control():`** Monitors the average current drawn by the pump and turns it OFF if the current exceeds or drops below specified limits.
- **`monitor_current():`** Continuously checks the current drawn by the pump.
- **`sync_time_periodically():`** Ensures that the ESP32's time is synchronized at regular intervals.
### 6. Main Loop:

**The main loop **`while True:`** continuously listens for incoming connections. When a request is received, it processes the request:**
- It checks available memory and collects garbage if necessary.
- It decodes the incoming request to determine if it is a POST request for updating settings or toggling GPIO pins.
- If the request is for updating settings, it extracts the parameters, updates the global variables, and saves the new settings to the file.
- If the request is for toggling pins, it toggles the state of the specified GPIO pin.
### 7. Generating and Sending the Response:

- After processing the request, the program generates an HTML response using the web_page() function, which displays the current status of the system, including RAM usage, average current, and GPIO states.
- The response is sent back to the client, and the connection is closed.
### 8. Continuous Operation:

- The program runs continuously, with the main loop handling web requests while the threaded functions manage time-based control and current monitoring in the background.
### Program Flow Conclusion:
> 🚦🚦🚦 **This structured flow ensures that the ESP32 operates effectively, allowing for real-time monitoring and control of the pump based on user-defined settings and current conditions. The combination of threaded functions and a responsive web server provides a robust solution for managing the pump system.** 🚦🚦🚦

## Get started with VScode PyMakr extension and knowing your specific ESP32  
> 🪔Im assuming youve already installed vscode. If not, install [VScode](https://code.visualstudio.com/download) . Then Python 3.9 or later is required, because youll be writing python scripts, just within the library confines of what micropython allows for your device. Also you'll need Node.js because PyMakr runs on Js.🪔

**Step 1: Install Python 3**
1. Go to the [official Python website](https://www.pythonguis.com/installation/install-python-windows/) and download the latest version of Python 3. Make sure to choose the version that matches your system (Windows 64-bit or 32-bit).

2. Open the downloaded file and run the installer.

3. **Installation Options: During the installation, make sure to check the box that says "Add Python to PATH". This will ensure that Python is added to your system's PATH environment variable, making it easier to run Python from the command line.**

4. Follow the rest of the prompts to complete the installation.

**Step 2: Verify Python Installation**
- Open Command Prompt: Press Win + R, type cmd, and press Enter.

- Check Python Version: Type `python --version` and press Enter. You should see the version of Python that you installed.

**Step 3: Install Node.js**
- Download Node.js: Go to the [official Node.js website](https://nodejs.org/en/download) and download the latest version of Node.js. Make sure to choose the version that matches your system (Windows 64-bit or 32-bit).

- Open the downloaded file and run the installer.

- Installation Options: During the installation, you can leave the default settings as they are. The installer will automatically add Node.js to your system's PATH environment variable.

- Follow the rest of the prompts to complete the installation.

**Step 4: Verify Node.js Installation**
- Open Command Prompt: Press Win + R, type cmd, and press Enter.

- Check Node.jsVersion: Type node -v and press Enter. You should see the version of Node.js that you installed.

- Check npm Version: Type npm -v and press Enter. You should see the version of npm (Node Package Manager) that comes with Node.js.

**Step 5: Manually Add Node.js to PATH (if needed)**
- Open Environment Variables Settings: Press Win + S, type "Environment Variables", and select "Edit the system environment variables".

- Edit System Variables: In the System Properties window, click on the "Environment Variables" button.

- Add Node.jsPath: In the "System variables" section, find the variable named "Path" and click "Edit". Click "New" and add the path to your Node.js installation (typically C:\Program Files\nodejs).

- Apply Changes: Click "OK" to close all the dialog boxes.

- Restart Command Prompt: Close and reopen the Command Prompt to apply the changes.

**Step 6: Verify PATH Variable**
- Open Command Prompt: Press Win + R, type cmd, and press Enter.

- Check PATH Variable: Type **`echo %PATH%`** and press Enter. Look for the Node.js path (C:\Program Files\nodejs) in the output.

**Step 7: Install the PyMakr Extension in VSCode**
1. Launch Visual Studio Code.

2. Install the Extension: Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing Ctrl + Shift + X.

3. Search for PyMakr: In the Extensions view, search for "PyMakr" and install the PyMakr extension.
![Pymakr-Install](/images/PyMakr%20Extention%20Install.jpg)

4. Reload VSCode: After installing the extension, a reload button should appear. Press it to reload VSCode1. Otherwise, close and re-open vscode.

**Step 8: Connect Your MicroPython Device & use esptool**
1. Connect Your Device: Connect your MicroPython device to your PC via USB.

2. Configure PyMakr: Follow the prompts provided by the PyMakr extension to set up your project folder and connect your device. You should typically have a boot.py, main.py & pymakr.conf file in your project folder. 

3. Finally using vscode terminal, install esptool **`pip install esptool`** and then add the install directory to your PATH so it can run freely in vscode.

4. Test your installation by running **`python -m esptool`** in your terminal.
- If esptool is installed, running python **`-m esptool`** without any additional arguments will display the help information for esptool. This will include a list of available commands and options that you can use with esptool.

- Executing Commands: To perform specific tasks, you need to include additional arguments. For example:

  - **`python -m esptool chip_id`** to read the chip ID.

  - **`python -m esptool flash_id`** to read the flash ID.

  - **`python -m esptool write_flash 0x00000 firmware.bin`** to write firmware to the device.
- 
> 🤜🤖🫷👉 **Very important fundamental: When you load the MicroPython firmware, you’re essentially installing the MicroPython interpreter onto your ESP32 device. This interpreter acts much like the BIOS firmware in a PC, setting up the environment to receive, interpret, and execute the code you write.**

> **The PyMakr plugin in your IDE then sends your Python scripts to the ESP32, where the onboard MicroPython interpreter runs them continuously. This setup streamlines the process of coding, testing, and deploying your Python projects.**

> **In the flashing command; 0x1000 is a crucial address within the ESP32's flash memory. Different devices or firmware versions might require different memory addresses for flashing. That’s why specifying the correct address in the command is so important. Your command makes sure the MicroPython firmware is written to the right place in memory, allowing it to function properly.** 👈😃👍🤖

**Step 9: Flash MicroPython Firmware**
1. Download Firmware: Go to the [MicroPython website](https://micropython.org/download/) and download the appropriate latest, stable firmware for your device. Keep in mind every device has its own special firmware. I used this firmwre for my generic [ESP32 WROOM](https://micropython.org/download/ESP32_GENERIC/)

> 🔎🔎🔎 **Ive added the .bin file for my ESP32 Wroom just for you to see, but make sure your downloaded version is inside your project folder. Then with terminal, navigate to you're project folder before proceeding.** 🔎🔎🔎 

2. Know your board & Flash Firmware: Follow the instructions provided by these sites. 

[randomnerdtutorials.com/flashing micropython firmware with esptool on esp32 & esp8266](https://randomnerdtutorials.com/flashing-micropython-firmware-esptool-py-esp32-esp8266/)

[micropython.org-Getting started with MicroPython on the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html) 

[espressif.com-Esptool.py Documentation](https://docs.espressif.com/projects/esptool/en/latest/esp32/)

[espressif.com-esp-dev-kits Documentation](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/)

**But this is what i found to work:** 
- Now double check your device COM port: In terminal type **`python -m serial.tools.list_ports`**. 
- **This gives me COM8, so i'll be using COM8 as an example, in my terminal commands. Im also going to add the linux commands below, just for you to be able to see the difference, when using windows from Linux.**

- To get your board info: **`python -m esptool -p COM8 flash_id`**
- If you are putting MicroPython on your board for the first time then you should first erase the entire flash by holding in the **"BOOT/FLASH"** button and using this command: 
```shell
for Linux: esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
for windows : python -m esptool --chip esp32 --port COM8 erase_flash  
```
- When the **“Erasing”** process begins, you can release the **“BOOT/FLASH”** button. After a few seconds, the ESP32 flash memory will be erased.

> 😨☝️ Note: If after the **“Connecting …”** message you keep seeing new dots appearing, it means that your ESP32 is not in flashing mode. You need to repeat all the steps described earlier and hold the “BOOT/FLASH” button again to ensure that your ESP32 goes into flashing mode and completes the erasing process successfully. 😨☝️

![esptool not in bootmode](/images/esptool%20no%20bootmode.jpg)

- It should look like this, when you've successfully entered **"Bootmode"**:

![esptool in Bootmode](/images/esptool%20in%20bootmode.jpg)

- From then on flash the firmware starting at address 0x1000 **(COM8, address and correct name of .bin is crucial):**

```shell
for Linux: esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin

for Windows: python -m esptool --chip esp32 --port COM8 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20241129-v1.24.1.bin

if you experience problems, load rather with normal speed and the verify command: python -m esptool --chip esp32 --port COM8 --baud 115200 write_flash -z 0x1000 ESP32_GENERIC-20241129-v1.24.1.bin --verify 
```
- If you are succesfull so far, the process will show you the progress in persentage:

![esptool busy flashing firmware onto the esp32](/images/esptool%20busy%20flashing.jpg)

- **If you are succesfull, you will see this. Yippeeeeeee, you're ESP now has micropython on it:**

![esptool done flashing firmware onto esp32](/images/esptool%20finished%20flashing.jpg)

> **Remember: This firmware goes into its own special memory area, so for any whatsoever reason you  need to reflash micropython onto your board, this will NOT erase your python project thats currently on it.** 

**Step 10: Using PyMakr to load your project onto the ESP32, and run it**

**Thank You DonskyTech!** 
This video helped me with getting started using the extention: [DonskyTech - Micropython using VScode PyMakr on ESP32](https://youtu.be/YOeV14SESls)

After the PyMakr2 installation, this is what you will see. with mine there's two icons in the activity bar. One for Pymakr devices, and another for the projects:



More information and tutorials can be found here:
- [docs.pycom.io](https://docs.pycom.io/)
- [github.com/sg-wireless/pymakr-vsc](https://github.com/sg-wireless/pymakr-vsc)
- [randomnerdtutorials.com Projects for esp32 & esp8266 in Micropython](https://randomnerdtutorials.com/projects-esp32-esp8266-micropython/)

