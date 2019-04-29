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
`python manage.py`

## Settings
First of all you should find the port your Arduino is connected to by looking under 
`tools > port` in your Arduino sketch application,
also you can list all serial ports available on your computer by running
`python -m serial.tools.list_ports` 

After finding the serial port your device is connected to, 
enter the port name in `settings.py` as a value of `serial_port_name`,
you can also change `serial_baudrate` and `serial_timeout` to your desired values.
