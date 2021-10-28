import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class QProgressIndicator(QWidget):
    def __init__(self, parent, stop_thread):
        super(QProgressIndicator, self).__init__(parent)
        self.initUI('Загружаем...')
        self.vb = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Всё работает, нужно немного подождать!')
        self.label.setWordWrap(True)
        self.vb.addWidget(self.label)

    def initUI(self, name):
        """Конструктор формы"""
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data\icon.ico'))
        self.show()



def TestProgressIndicator(stop_thread):
    app = QApplication(sys.argv)
    progress = QProgressIndicator(None, stop_thread)


    sys.exit(app.exec_())


if __name__ == "__main__":
    stop_thread = False
    TestProgressIndicator(stop_thread)
