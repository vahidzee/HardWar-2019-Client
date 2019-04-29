def load_settings(file_name='settings.py'):
    """
    executes given file and returns its lexical vocabulary
    as a python dictionary
    """
    namespace = dict()
    with open(file_name) as handle:
        exec(handle.read(), namespace)
    return namespace


# Loading Settings
settings = load_settings()

# while True:
#     # Getting input
#     command = input('\033[32;0mCommand : \033[0m')
#
#     if command == 'exit':
#         exit()

import Serial.connection as ser_con

serial_connection = ser_con.Connection(
    serial_port_name=settings['serial_port_name'],
    baudrate=settings['serial_baudrate'],
    timeout=settings['serial_timeout']
)

serial_connection.listener(1)
