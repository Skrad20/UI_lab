from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QDesktopWidget, QDialog, QFormLayout, QLineEdit,
    QCheckBox, QPushButton
)


class FormEnterFarmName(QDialog):
    def __init__(self, name, parent=None) -> None:
        super(FormEnterFarmName, self).__init__(parent)
        self.initUI(name)
        self.le = QLineEdit()
        self.pb = QPushButton()
        self.pb.setText("Ввести название хозяйства")
        layout = QFormLayout()
        self.res_mutter_analis = False
        self.check_box = QCheckBox("Подбирать матерей.")
        self.check_box.stateChanged.connect(
                lambda checked,
                res=name: self.check_box_answer(checked, res)
            )
        layout.addWidget(self.le)
        layout.addWidget(self.pb)
        layout.addWidget(self.check_box)
        self.setLayout(layout)
        self.pb.clicked.connect(self.button_click)
        self.setWindowTitle("example")

    def check_box_answer(self, checked, res):
        "Сохраняет текст в свойствах класса"
        self.res_mutter_analis = bool(checked)

    def button_click(self) -> list:
        '''
        Возвращает название хозяйства и булевое значение
        необходимости обработки матерей
        '''
        self.text = self.le.text()
        self.close()
        return self.text, self.res_mutter_analis

    def initUI(self, name: str) -> None:
        """Конструктор формы"""
        self.center()
        self.setFixedSize(400, 300)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.show()

    def center(self) -> None:
        """Центрирует окно"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().topLeft()
        qr.moveCenter(cp)
        self.move(qr.center())
