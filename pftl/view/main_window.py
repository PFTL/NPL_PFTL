

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5.QtCore import QTimer


from pftl.model.experiment import Experiment
from pftl.view.monitor_window import MonitorWindow

from pathlib import Path

class ScanWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        this_path = Path(__file__).parent
        uic.loadUi(this_path/'main_window.ui', self)
        self.experiment = experiment

        self.button_1.clicked.connect(self.button_clicked)
        self.button_2.clicked.connect(self.stop_scan)

        self.line_start.setText(str(self.experiment.config['Scan']['start']))
        self.line_stop.setText(str(self.experiment.config['Scan']['stop']))
        self.line_step.setText(str(self.experiment.config['Scan']['step']))

        self.actionSave_Data.triggered.connect(self.save_data)

        self.line = self.plot_widget.plot([0], [0])
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.timeout.connect(self.update_value)
        self.plot_timer.start(30)  # Time in milliseconds!

        self.monitor_window = MonitorWindow(self.experiment)
        self.actionShow_Monitor.triggered.connect(self.monitor_window.show)

    def save_data(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", None)
        self.experiment.config['Data']['folder'] = folder
        self.experiment.save_data()

    def update_value(self):
        last_value = self.experiment.last_value
        self.line_value.setText(f'{last_value:1.3f}')

    def update_plot(self):
        self.line.setData(self.experiment.scan_voltages[:self.experiment.i], self.experiment.measured_voltages[
                                                                             :self.experiment.i])

    def button_clicked(self):
        print(self.line_start.text())
        print(self.line_stop.text())

        self.experiment.config['Scan']['start'] = float(self.line_start.text())
        self.experiment.config['Scan']['stop'] = float(self.line_stop.text())
        self.experiment.config['Scan']['step'] = float(self.line_step.text())
        self.experiment.start_scan()
        print('Button Clicked')

    def stop_scan(self):
        self.experiment.stop_scan()

    def closeEvent(self, *args, **kwargs):
        self.monitor_window.close()
        self.experiment.finalize()
        super().closeEvent(*args, **kwargs)


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('../../Examples/config.yml')
    exp.load_daq()

    app = QApplication([])
    win = ScanWindow(exp)
    win.show()
    app.exec()