import serial


class Connection:
    # variables
    output_streams = []

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

    def listener(self, size: int = 1):
        while True:
            print(self.port.read(size=size))
