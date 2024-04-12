from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton


def button_clicked():
    print('Button Clicked')


app = QApplication([])
win = QMainWindow()

button = QPushButton("Click Me", win)
button.clicked.connect(button_clicked)

win.show()
app.exec()