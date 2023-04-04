from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QToolBar, QGridLayout, QHBoxLayout, QMenuBar, QMenu, QFileDialog,
    QLabel, QMainWindow, QMessageBox,
    QSplashScreen, QTableWidget, QPushButton,QAction
)

from setting import IS_TEST as is_test

adres_job = ''
data_job = ''
adres_job_search_father = ''
stop_thread = False


class GeneralWindow(QMainWindow):
    """Управляет окнами программы."""
    def __init__(self) -> None:
        super(GeneralWindow, self).__init__()
        self.setWindowTitle("BioTechLab")

        self._create_statusbar()
        self._create_geometry()
        self._create_actions()
        self._create_tool_bar()

    def _create_statusbar(self):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready", 3000)

    def _create_geometry(self):
        self.resize(600, 400)
        self.centralWidget = QLabel(
            'Добро пожаловать!'
        )
        self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.centralWidget)

    def _create_tool_bar(self):
        tool_bar = QToolBar("Work", self)
        tool_bar.setMovable(True)
        for ation in self.list_action:
            tool_bar.addAction(ation)
        self.addToolBar(Qt.LeftToolBarArea, tool_bar)

    def _create_actions(self):
        self.list_action = []
        dict_actions = {
            "Анализ МС": self.analys_ms,
            "Анализ ISSR": self.analys_issr,
            "Обновление базы данных": self.update_base_data,
            "О программе": self.about,
            "Тест": self.start_test,
        }
        for text, func in dict_actions.items():
            action = QAction(text, self)
            action.triggered.connect(func)
            action.setStatusTip("Будет подсказка")
            action.setToolTip("Будет подсказка")
            self.list_action.append(action)

    def analys_ms(self):
        self.setCentralWidget(WidgetMS(self.statusbar))
        self.statusbar.showMessage("Анализ данных", 3000)

    def analys_issr(self):
        self.setCentralWidget(WidgetISSR())

    def update_base_data(self):
        self.setCentralWidget(WidgetUpdateDB())

    def about(self):
        self.setCentralWidget(WidgetAbout())

    def start_test(self):
        self.setCentralWidget(WidgetTest())


class BaseWindow(QWidget):
    def __init__(self, statusbar=None, *args, **kwargs):
        super(BaseWindow, self).__init__(*args, **kwargs)
        self.statusbar = statusbar
        self.dict_widget = {}
        self._create_actions()
        self._create_labels()
        self._create_tool_bar()
        self._create_layout()

    def _create_layout(self):
        layout = QHBoxLayout(self)
        for key, val in self.dict_widget:
            layout.addWidget(key, *val)
        self.setLayout(layout)

    def _create_tool_bar(self):
        pass

    def _create_actions(self):
        pass

    def _create_labels(self):
        pass


class WidgetMS(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dict_widget = {
            self.tool_bar: []
        }

    def _create_tool_bar(self):
        self.tool_bar = QToolBar("Work", self)
        self.tool_bar.setMovable(True)
        for action in self.list_action:
            self.tool_bar.addAction(action)

    def _create_actions(self):
        self.list_action = []
        dict_actions = {
            "Генетические паспорта": self.gen_password,
            "Подбор отцов": self.search_father
        }
        for text, func in dict_actions.items():
            action = QAction(text, self)
            action.triggered.connect(func)
            self.list_action.append(action)

    def gen_password(self):
        self.statusbar.showMessage("Идёт анализ", 3000)
        WidgetGenPass(self)
        
        self.statusbar.showMessage("Анализ окончен", 3000)

    def search_father(self):
        print("test")


class WidgetGenPass(BaseWindow):
    def __init__(self, statusbar=None, *args, **kwargs):
        super().__init__(statusbar, *args, **kwargs)
        self.dict_widget = {
            self.list_label[0]: []
        }

    def _create_labels(self):
        self.list_label = []
        lebels = [
            "Генетические паспорта"
        ]
        for text in lebels:
            label = QLabel(text, self)
            self.list_label.append(label)


class WidgetISSR(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WidgetUpdateDB(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WidgetTest(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WidgetAbout(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
