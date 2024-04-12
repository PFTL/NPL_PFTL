from time import sleep
from serial import Serial


class SerialDAQ:
    def __init__(self, port):
        self.port = port
        self.dev = None
        self.serial_number = ''

    def initialize(self):
        self.dev = Serial(self.port)
        sleep(.5)

    def finalize(self):
        self.dev.close()

    def query(self, message):
        if self.dev is None:
            raise Exception('You must first initialize the device with initialize()')

        message = message + "\n"
        message = message.encode()
        self.dev.write(message)
        return self.dev.readline().decode('ascii').strip()

    def idn(self):
        self.serial_number = self.query('*IDN?')

    def set_analog_value(self, channel, value):
        if value > 4095:
            raise ValueError('Value should be < 4095')
        if channel not in (0, 1):
            raise ValueError('Channel should be either 0 or 1')

        message = f'OUT:CH{channel} {value}'
        self.query(message)

    def read_analog(self, channel):
        message = f'MEAS:CH{channel}?'
        return int(self.query(message))


if __name__ == "__main__":
    dev = SerialDAQ('/dev/cu.usbmodem11101')
    dev.initialize()
    print(dev.serial_number)
    dev.set_analog_value(0, 4095)
    # for i in range(4000):
    #     dev.set_analog_value(0, i)
    #     current.append(dev.read_analog(0))
    dev.finalize()