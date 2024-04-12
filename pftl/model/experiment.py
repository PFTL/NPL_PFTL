import datetime
import time

from pathlib import Path
from threading import Thread

import numpy as np
import yaml

from pftl.model.analog_daq import AnalogDAQ
from pftl.model.dummy_daq import DummyDAQ


class Experiment:
    def __init__(self):
        self.config = {}
        self.daq = None
        self.scan_voltages = np.empty((1, ))
        self.measured_voltages = np.empty((1, ))
        self.monitored_voltages = np.empty((1, ))
        self.scan_running = False
        self.i = 0
        self.last_value = 0

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f, yaml.FullLoader)

    def load_daq(self):
        if self.config['DAQ']['model'] == "Real":
            self.daq = AnalogDAQ(self.config['DAQ']['port'])
        elif self.config['DAQ']['model'] == "Dummy":
            self.daq = DummyDAQ(self.config['DAQ']['port'])
        else:
            raise Exception("DAQ Not supported")

    def do_monitor(self):
        if self.scan_running:
            print("Scan or Monitor already running.")
            return

        self.scan_running = True
        self.monitored_voltages = np.zeros((self.config['Monitor']['length']))

        self.keep_monitoring = True
        while self.keep_monitoring:
            value = self.daq.read_voltage(self.config['Monitor']['channel_in'])
            self.monitored_voltages = np.roll(self.monitored_voltages, -1)
            self.monitored_voltages[-1] = value

        self.scan_running = False

    def start_monitor(self):
        self.monitor_thread = Thread(target=self.do_monitor)
        self.monitor_thread.start()

    def stop_monitor(self):
        self.keep_monitoring = False

    def do_scan(self):
        if self.scan_running:
            print("Scan already running.")
            return

        self.scan_running = True

        self.scan_voltages = np.arange(self.config['Scan']['start'],
                                  self.config['Scan']['stop']+self.config['Scan']['step'],
                                  self.config['Scan']['step'])
        self.measured_voltages = np.zeros_like(self.scan_voltages)

        self.keep_scanning = True
        for self.i in range(len(self.scan_voltages)):
            if not self.keep_scanning:
                break
            voltage = self.scan_voltages[self.i]
            self.daq.set_voltage(self.config['Scan']['channel_out'], voltage)
            self.last_value = self.daq.read_voltage(self.config['Scan']['channel_in'])
            self.measured_voltages[self.i] = self.last_value

        self.scan_running = False

    def start_scan(self):
        self.scan_thread = Thread(target=self.do_scan)
        self.scan_thread.start()

    def stop_scan(self):
        self.keep_scanning = False

    def save_data(self):
        folder_date = f'{datetime.date.today()}'
        base_folder = Path(self.config['Data']['folder'])

        save_dir = base_folder / folder_date

        save_dir.mkdir(parents=True, exist_ok=True)

        data = np.vstack((self.scan_voltages, self.measured_voltages))

        filename = Path(self.config['Data']['filename'])
        i = 1
        new_filename = f'{filename.stem}_{i}{filename.suffix}'
        full_path = save_dir / new_filename
        while full_path.exists():
            i += 1
            new_filename = f'{filename.stem}_{i}{filename.suffix}'
            full_path = save_dir / new_filename

        np.savetxt(full_path, data, delimiter=',')

        metadata_filename = Path(self.config['Data']['metadata_filename'])
        metadata_filename = f'{metadata_filename.stem}_{i}{metadata_filename.suffix}'
        self.save_metadata(save_dir/metadata_filename)

    def save_metadata(self, file_path):
        with open(file_path, 'w') as f:
            yaml.dump(self.config, f)

    def finalize(self):
        self.stop_scan()
        self.stop_monitor()
        while self.scan_running:
            time.sleep(0.1)
        self.daq.finalize()


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('../../Examples/config.yml')
    print(exp.config)
    exp.load_daq()
    print(exp.daq)
    exp.do_scan()
    print(exp.measured_voltages, exp.scan_voltages)
    exp.save_data()
