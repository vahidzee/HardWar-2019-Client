import serial
import multiprocessing as mp
import datetime


class Connection:
    # variables
    output_streams = []
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
        self.port = serial.Serial(
            serial_port_name,
            baudrate=baudrate,
            timeout=timeout
        )

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
                data = self.port.read(size)
                if data:
                    # logging data
                    if log:
                        print(
                            f'\033[32;0mSerial\033[0m {self.port.name:^30}',
                            f'\033[32;0mTime\033[0m \033[34;0m{datetime.datetime.now().time()}\033[0m',
                            '\033[32;0m:\033[0m',
                            data
                        )

                    # sending data to every output stream
                    for stream in self.output_streams:
                        stream.send(data)

        self.active_listener = mp.Process(
            target=listener_process,
            name='listener' + self.port.name,
            daemon=False
        )
        self.active_listener.start()
