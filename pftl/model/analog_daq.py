from pftl.controller.serial_daq import SerialDAQ


class AnalogDAQ:
    def __init__(self, port):
        self.port = port
        self.driver = SerialDAQ(self.port)
        self.driver.initialize()
        self.driver.idn()

    def set_voltage(self, channel, volts):
        volt_bits = int((2**12-1)/3.3*volts)
        self.driver.set_analog_value(channel, volt_bits)

    def read_voltage(self, channel):
        volt_bits = self.driver.read_analog(channel)
        volts = volt_bits/(2**10-1)*3.3
        return volts

    def finalize(self):
        self.driver.set_analog_value(0, 0)
        self.driver.set_analog_value(1, 0)
        self.driver.finalize()

    def __str__(self):
        return f"AnalogDAQ, serial: {self.driver.serial_number}, on port: {self.port}"


if __name__ == "__main__":
    analog_daq = AnalogDAQ("/dev/cu.usbmodem11101")
    print(analog_daq)
    analog_daq.set_voltage(0, 3.3)
    print(f'Measured voltage: {analog_daq.read_voltage(0)}')
    analog_daq.set_voltage(2, 3.3)
    analog_daq.finalize()

