from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDesktopWidget, QDialog, QFormLayout, QLineEdit,
                             QPushButton)


class Form(QDialog):
    def __init__(self, name, parent=None) -> None:
        super(Form, self).__init__(parent)
        self.initUI(name)
        self.le = QLineEdit()
        self.pb = QPushButton()
        self.pb.setText("Ввести название хозяйства")
        layout = QFormLayout()
        layout.addWidget(self.le)
        layout.addWidget(self.pb)
        self.setLayout(layout)
        self.pb.clicked.connect(self.button_click)
        self.setWindowTitle("example")

    def button_click(self) -> None:
        '''Сохранение текста'''
        self.text = self.le.text()
        self.close()
        return self.text

    def initUI(self, name: str) -> None:
        """Конструктор формы"""
        self.center()
        self.setFixedSize(400, 150)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.show()

    def center(self) -> None:
        """Центрирует окно"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().topLeft()
        qr.moveCenter(cp)
        self.move(qr.center())
