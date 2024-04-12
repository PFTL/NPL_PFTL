from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyqtgraph as pg

from pftl.model.experiment import Experiment


class MonitorWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment

        self.control_widget = QWidget(self)
        self.start_button = QPushButton("Start", self)
        self.stop_button = QPushButton("Stop", self)
        self.channel_line = QLineEdit(self)

        self.channel_line.setText(str(self.experiment.config['Monitor']['channel_in']))

        self.start_button.clicked.connect(self.experiment.start_monitor)
        self.stop_button.clicked.connect(self.experiment.stop_monitor)

        layout = QHBoxLayout()
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.channel_line)
        self.control_widget.setLayout(layout)

        self.plot_widget = pg.PlotWidget()

        self.central_widget = QWidget(self)
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.control_widget)
        central_layout.addWidget(self.plot_widget)
        self.central_widget.setLayout(central_layout)

        self.setCentralWidget(self.central_widget)

        self.plot = self.plot_widget.plot([0], [0])

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.start(30)

        self.channel_line.editingFinished.connect(self.update_params)

    def update_params(self):
        self.experiment.config['Monitor']['channel_in'] = int(self.channel_line.text())
        print(f'Updated channel_in to {self.channel_line.text()}')

    def update_plot(self):
        self.plot.setData(self.experiment.monitored_voltages)

    def closeEvent(self, *args, **kwargs):
        self.experiment.stop_monitor()
        super().closeEvent(*args, **kwargs)



if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('../../Examples/config.yml')
    exp.load_daq()

    app = QApplication([])
    monitor = MonitorWindow(exp)
    monitor.show()
    app.exec()