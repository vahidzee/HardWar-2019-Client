# general imports
import serial
import multiprocessing as mp
import datetime
import time
import socket


class NetworkConnection:
    def __init__(
            self,
            server_address: str,
            server_port: int,
            log: bool = False
    ):
        self.server_address = (server_address, server_port)
        self.log = log
        # opening network socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as e:
            print(f"\033[31;0mUnable to open TCP socket - {e}\033[0m")
            exit()

        # connecting socket to server
        print(f'Connecting to address: {server_address:^30} - port: {server_port:^6}')
        try:
            self.sock.connect((server_address, server_port))
        except Exception as e:
            print(
                f"\033[31;0mUnable to connect socket to the given address {server_address:^20}:{server_port:^6} - {e}\033[0m"
            )
            exit()

    def receive_data(self, size: int = 16):
        """
        a blocking function to receive data
        """
        recieved_data = self.sock.recv(size)
        if self.log:
            print(
                f'\033[32;0mTCP Connection',
                f'\033[32;0mTime\033[0m \033[34;0m{datetime.datetime.now().time()}\033[0m',
                '\033[32;0m:\033[0m',
                recieved_data.hex()
            )
        return recieved_data

    def send_data(self, data):
        try:
            self.sock.send(data)
        except Exception as e:
            print(
                f"\033[31;0mUnable to Send data through TCP connection to server. Connection Lost - {e}\033[0m"
            )
            exit()


class SerialConnection:
    active_listener = None
    network_connection = None

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
        except Exception as e:
            print(
                f"\033[31;0mUnable to make serial connection to port {serial_port_name} - {e}\033[0m"
            )
            exit()

    def set_network_connection(self, network_connection: NetworkConnection):
        self.network_connection = network_connection

    def send_data(self, data):
        try:
            self.port.write(data)
        except Exception as e:
            print(
                f"\033[31;0mUnable to send data to serial connection {self.port.name} - {e}\033[0m"
            )
            exit()

    def start_listener(
            self,
            size: int = 5,
            log: bool = True
    ):
        """
        creates a listener process for this connection
        """

        # checking if any active listener process exists
        if self.active_listener:
            self.active_listener.kill()

        def listener_process():
            """
            reads data and sends data to received data processor function
            """
            while True:
                # waiting for network data if available
                if self.network_connection:
                    network_data = self.network_connection.receive_data()

                    # forwarding received network data to Arduino
                    self.send_data(network_data)

                data = None
                while self.port.in_waiting >= size:
                    data = self.port.read(size)
                if data:
                    # logging data
                    if log:
                        print(
                            f'\033[32;0mSerial\033[0m {self.port.name:^30}',
                            f'\033[32;0mTime\033[0m \033[34;0m{datetime.datetime.now().time()}\033[0m',
                            '\033[32;0m:\033[0m',
                            data.hex()
                        )

                    # processing received data
                    self.process_recieved_data(data)

        # resetting Arduino before starting listener process
        print("Signalling Arduino to reset ...")
        self.reset_arduino()

        print("Startin Serial Connection Process")
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
        """
        sends reset signal to connected arduino
        """
        # Toggle DTR to reset Arduino
        self.port.setDTR(False)

        # waiting for arduino to boot
        time.sleep(0.3)

        # tossing any data already received, see
        self.port.flushInput()
        self.port.setDTR(True)

    def process_recieved_data(self, data):
        # validating input data
        if data[0] != 0x55 or data[4] != 0xAA:
            return None

        # local variables
        processed_data = bytearray(2)
        thr = 40

        # processing joystick direction
        if data[1] > 128 + thr:  # Left
            processed_data[0] = 0
        elif data[1] < 128 - thr:  # Right
            processed_data[0] = 1
        elif data[2] > 128 + thr:  # Up
            processed_data[0] = 2
        elif data[2] < 128 - thr:  # Down
            processed_data[0] = 3
        else:
            processed_data[0] = 4

        if data[3] == 0xFF:  # Button
            processed_data[1] = 1
        else:
            processed_data[1] = 0

        # sending data to network connection if available
        if self.network_connection:
            self.network_connection.send_data(processed_data)
