# general imports
import sys

# project imports
import src.methods

# loading settings
src.methods.load_settings()

if len(sys.argv) >= 2:
    if sys.argv[1] == 'debug_arduino':
        src.methods.debug_arduino()

    else:
        print("\033[31;0mOption is not available\033[0m")
else:
    src.methods.bind_serial_and_network()
