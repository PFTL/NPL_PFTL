import sys
from PyQt5.QtWidgets import QApplication

from pftl.model.experiment import Experiment
from pftl.view.main_window import ScanWindow


def start():
    exp = Experiment()
    exp.load_config(sys.argv[1])
    exp.load_daq()

    app = QApplication([])
    win = ScanWindow(exp)
    win.show()
    app.exec()


if __name__ == "__main__":
    start()