from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QToolBar, QGridLayout, QHBoxLayout, QMenuBar, QMenu, QFileDialog,
    QLabel, QMainWindow, QMessageBox, QLineEdit, QTextEdit,
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
        self.dict_widgets = {}
        self.list_actions = []
        self.list_labels = []
        self.list_tool_bar = []
        self._create_actions()
        self._create_labels()
        self._create_tool_bar()
        self._create_layout()

    def _create_layout(self):
        pass

    def _create_tool_bar(self):
        pass

    def _create_actions(self):
        pass

    def _create_labels(self):
        pass


class WidgetMS(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create_layout(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.tool_bar, 0, 0)
        self.setLayout(self.grid)
        self.show()

    def _create_tool_bar(self):
        self.tool_bar = QToolBar("Gene", self)
        self.tool_bar.setMovable(True)
        for ation in self.list_action:
            self.tool_bar.addAction(ation)

    def _create_actions(self):
        self.list_action = []
        dict_actions = {
            "Создание поспартов": self.gen_password,
            "Подбор отца": self.search_father,
        }
        for text, func in dict_actions.items():
            action = QAction(text, self)
            action.triggered.connect(func)
            action.setStatusTip("Будет подсказка")
            action.setToolTip("Будет подсказка")
            self.list_action.append(action)

    def _create_labels(self):
        pass

    def gen_password(self):
        self.statusbar.showMessage("Идёт анализ", 3000)
        window = WidgetGenPass(self)        
        self.grid.addWidget(window)

        self.statusbar.showMessage("Анализ окончен", 3000)

    def search_father(self):
        self.statusbar.showMessage("Идёт анализ", 3000)
        window = WidgetSarchFather(self)
        self.grid.
        self.grid.addWidget(window)

        self.statusbar.showMessage("Анализ окончен", 3000)


class WidgetGenPass(BaseWindow):
    def __init__(self, statusbar=None, *args, **kwargs):
        super().__init__(statusbar, *args, **kwargs)
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        self.setLayout(grid)


class WidgetSarchFather(BaseWindow):
    def __init__(self, statusbar=None, *args, **kwargs):
        super().__init__(statusbar, *args, **kwargs)
        title = QLabel('Tama')
        author = QLabel('Tuta')
        review = QLabel('Kuka')
        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        self.setLayout(grid)


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
