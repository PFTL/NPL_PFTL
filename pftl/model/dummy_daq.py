import numpy as np
from time import sleep


class DummyDAQ:
    def __init__(self, port):
        self.port = port

    def set_voltage(self, channel, volts):
        pass

    def read_voltage(self, channel):
        sleep(.01)
        return np.random.random()

    def finalize(self):
        pass

    def __str__(self):
        return f"Dummy DAQ on port: {self.port}"