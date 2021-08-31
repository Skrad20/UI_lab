import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton


class Window1(QWidget):
    def __init__(self):
        super(Window1, self).__init__()
        self.setWindowTitle('Window1')
        self.setMinimumWidth(200)
        self.setMinimumHeight(50)
        self.button = QPushButton(self)
        self.button.setText('Открыть второе окно')
        self.button.show()


class Window2(QWidget):
    def __init__(self):
        super(Window2, self).__init__()
        self.setWindowTitle('Window2')
        


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('MainWindow')

    def show_window_1(self):
        self.w1 = Window1()
        self.w1.button.clicked.connect(self.show_window_2)
        self.w1.button.clicked.connect(self.w1.close)
        self.w1.show()

    def show_window_2(self):
        self.w2 = Window2()
        self.w2.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show_window_1()
    sys.exit(app.exec_())