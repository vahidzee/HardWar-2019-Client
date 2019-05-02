# Hardwar 2019 - Arduino Middleware Client
## Setup
Python 3.5 or higher is required

Follow the steps bellow:
1. Clone this repository by running :
`git clone www.github.com/vahidzee/HardWarClient.git`

2. Create a virtual environment for the project by running : 
`virtualenv --python=python3 venv`

3. Activate your virtual environment by running:
`source venv/bin/activate`

4. Install Project requirements by running:
`pip install -r requirments.txt`

5. Run Project by running:
`python main.py`

## Settings
### Serial Port Setup
First of all you should find the port your Arduino is connected to by looking under 
`tools > port` in your Arduino sketch application,
also you can list all serial ports available on your computer by running
`python -m serial.tools.list_ports` 

After finding the serial port your device is connected to, 
enter the port name in `settings.py` as a value of `serial_port_name`,
you can also change `serial_baudrate` and `serial_timeout` to your desired values.

### Network Address
Set `server_address` and `server_port` to announced values.

### Log Settings
If `serial_log` is set to `True`, every Serial output of your Arduino device will be displayed in both two running modes.

If `network_log` is set to `True`, every received data from server will be displayed in both two running modes.
 
## Usage
### Running options
There are Two Running Options:
1. Binding Arduino to the network: `python main.py` which binds your Arduino device to the server specified by `server_address` and `server_port` in settings.
2. Debugging Arduino's Connection: `python main.py debug_arduino` which sends the byte-array set by `arduino_debug_message` in `settings.py` file.

### Accessing Data From Arduino's Side
Every data sent to your device is accessible through Arduino's Serial read methods and all your Serial output results will be read by Client Application.


## Debugging Windows Problems
* First of all make sure you're typing `py` instead of `python` to run python applications :D !
* Make sure you're running this project as an administrator (open your command line application as an administrator)
* If you're still getting errors while opening the serial port, goto your `device manager` and `disable` and `enable` the serial port your device is connected to without pulling it out.
