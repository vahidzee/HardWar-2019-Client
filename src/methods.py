# project imports
from .connections import SerialConnection, NetworkConnection

# global variables
settings = None
serial_connection = None
network_connection = None


def load_settings(file_name='settings.py'):
    """
    executes given file and returns its lexical vocabulary
    as a python dictionary
    """
    global settings
    print("Loading Settings")

    namespace = dict()
    with open(file_name) as handle:
        exec(handle.read(), namespace)

    settings = namespace
    return namespace


def start_serial_connection():
    global serial_connection, settings

    serial_connection = SerialConnection(
        settings['serial_port_name'],
        settings['serial_baudrate'],
        settings['serial_timeout']
    )


def start_network_connection():
    global network_connection, settings

    network_connection = NetworkConnection(
        settings['server_address'],
        settings['server_port'],
        settings['network_log']
    )


def bind_serial_and_network():
    global settings
    start_serial_connection()
    start_network_connection()

    global network_connection, serial_connection

    serial_connection.set_network_connection(network_connection)

    serial_connection.start_listener(
        log=settings['serial_log']
    )


def debug_arduino():
    start_serial_connection()

    global serial_connection

    serial_connection.start_listener(
        log=settings['serial_log'],
        debug_message=settings['arduino_debug_message']
    )
