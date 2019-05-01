# Serial port Settings
serial_port_name = '/dev/ttyACM0'
serial_baudrate = 9600
serial_timeout = None

# Network Settings
server_address = '192.168.200.83'
server_port = 6666

# Log settings
serial_log = False
network_log = False

# Teams info
team_id = -1
team_name = ""

# Arduino debug message
arduino_debug_message = bytearray(
    [0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA, 0x55, 0xAA,
     0x55])
