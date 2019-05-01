import serial
import multiprocessing as mp
import datetime
from settings import sample_2_arduino_data
import time



class Connection:
    # variables
    # output_streams = []
    active_listener = None

    def __init__(
            self,
            serial_port_name: str,
            baudrate: int = 9600,
            timeout: int = 0
    ):
        """
        opens serial connection to the specified serial_port
        """
        try:
            self.port = serial.Serial(
                serial_port_name,
                baudrate=baudrate,
                timeout=timeout
            )
        except:
            print("Error: can't find the Port:",serial_port_name)
            print("Probable Solution:")
            print("1. Find the port name by running: python -m serial.tools.list_ports")
            print("2. Change the port name in the settings.py file")
            exit()


    def add_output_stream(self, output_stream):
        pass

    def start_listener(
            self,
            size: int = 4,
            log: bool = True
    ):
        """
        creates a listener process for this connection
        """

        # checking if any active listener process exists
        if self.active_listener:
            self.active_listener.kill()

        def bytes_to_int(bytes):
            result = 0

            for b in bytes:
                result = result * 256 + int(b)

            return result

        def listener_process():
            """
            reads data and sends it to every output stream of this serial connection
            """
            while True:
                # Here the blocking TCP socket will wait for a new packet from the server
                time.sleep(0.1)
                self.port.write(sample_2_arduino_data)

                data = None
                while self.port.in_waiting >= 5:# will update until the last packet will be received
                    data = self.port.read(5)
                if data:
                    # logging data
                    if log:
                        print(
                            f'\033[32;0mSerial\033[0m {self.port.name:^30}',
                            f'\033[32;0mTime\033[0m \033[34;0m{datetime.datetime.now().time()}\033[0m',
                            '\033[32;0m:\033[0m',
                            data.hex()
                        )

                    # # sending data to every output stream
                    # for stream in self.output_streams:
                    #     stream.send(data)
                else:# Arduino didn't send any message
                    print("No messages from Arduino")


        print("Signal arduino to reset")
        self.reset_arduino()

        self.active_listener = mp.Process(
            target=listener_process,
            name='listener' + self.port.name,
            daemon=False
        )
        try:
            self.active_listener.start()
        except serial.serialutil.SerialException:
            print("Error, lost the connection of the arduino")


    def reset_arduino(self):
        # Toggle DTR to reset Arduino
        self.port.setDTR(False)
        time.sleep(0.3)
        # toss any data already received, see
        # http://pyserial.sourceforge.net/pyserial_api.html#serial.Serial.flushInput
        self.port.flushInput()
        self.port.setDTR(True)
