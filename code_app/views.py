from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel
from PyQt5.QtWidgets import (
    QWidget, QToolBar, QGridLayout, QDialog, QMenuBar, QMenu, QFileDialog,
    QLabel, QMainWindow, QMessageBox, QLineEdit, QTextEdit, QTableView,
    QSplashScreen, QTableWidget, QPushButton, QAction, QComboBox,
    QVBoxLayout, QRadioButton, QButtonGroup, QCheckBox
)
from .managers import ManagerDataMS, ManagerDB
from .models import  Cow, Deer, Sheep
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
        
        self.manager_db = ManagerDB()
        self.statusbar = statusbar
        self.dict_widgets = {}
        self.list_actions = []
        self.list_labels = []
        self.list_tool_bar = []
        self._create_actions()
        self._create_labels()
        self._create_tool_bar()
        self._create_buttons()
        self._create_radio_buttons()
        self._create_check_box()
        self._create_text_edit()
        self._create_combo_box()
        self._create_layout()
    
    def _create_combo_box(self):
        pass

    def _create_text_edit(self):
        pass

    def _create_layout(self):
        pass

    def _create_tool_bar(self):
        pass

    def _create_actions(self):
        pass

    def _create_labels(self):
        pass

    def _create_radio_buttons(self):
        pass

    def _create_buttons(self):
        pass

    def _create_check_box(self):
        pass


class WidgetMS(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget_start = None

    def _create_layout(self):
        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignTop)
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
            "Создание паспортов": [
                self.gen_password,
                "Генерация паспортов в документ WORD",
                "Нажмите"
            ],
            "Подбор отца": [self.search_father, "", ""],
        }
        for text, value in dict_actions.items():
            action = QAction(text, self)
            action.triggered.connect(value[0])
            action.setStatusTip(value[1])
            action.setToolTip(value[2])
            self.list_action.append(action)

    def _create_labels(self):
        pass

    def gen_password(self):
        self.statusbar.showMessage("Идёт анализ", 3000)
        window = WidgetGenPass(self)
        if self.widget_start is None:
            self.widget_start = window
            self.grid.addWidget(self.widget_start)
        else:
            widget_out = self.grid.replaceWidget(self.widget_start, window)
            widget_out.widget().deleteLater()
            self.widget_start = window
        self.statusbar.showMessage("Анализ окончен", 3000)

    def search_father(self):
        self.statusbar.showMessage("Идёт анализ", 3000)
        window = WidgetSarchFather(self)
        if self.widget_start is None:
            self.widget_start = window
            self.grid.addWidget(self.widget_start)
        else:
            widget_out = self.grid.replaceWidget(self.widget_start, window)
            widget_out.widget().deleteLater()
            self.widget_start = window
        self.statusbar.showMessage("Анализ окончен")


class WidgetGenPass(BaseWindow):
    def __init__(self, statusbar=None, *args, **kwargs):
        self.manager_ms = None
        self.species_animal = "bos_taurus"
        super().__init__(statusbar, *args, **kwargs)

    def _create_layout(self):
        title = QLabel('Создание генетических паспортов')
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(title, 0, 0)
        for i, elem in enumerate(self.list_check_box):
            self.grid.addWidget(elem, i, 1)
        for i, elem in enumerate(self.list_radio_button):
            self.grid.addWidget(elem, i+1, 0)
        for i, elem in enumerate(self.list_buttons):
            self.grid.addWidget(elem, i+1, 1)
        self.grid.addWidget(self.combobox, 5, 0)
        self.setLayout(self.grid)

    def _create_buttons(self):
        self.list_buttons = []
        dict_buttons = {
            "Открыть файл описи": [self.open_file_invertory, "", ""],
            "Открыть файл генотипов": [self.open_file_profils, "", ""],
            "Открыть таблицу для ввода описи": [
                self.open_table_invertory, "", ""
            ],
            "Открыть таблицу для ввода генотипов": [
                self.open_table_profils, "", ""
            ],
            "Создать паспорта": [self.start_pipline_gen_password, "", ""]
        }
        for text, value in dict_buttons.items():
            button = QPushButton(text, self)
            button.clicked.connect(value[0])
            button.setStatusTip(value[1])
            button.setToolTip(value[2])
            self.list_buttons.append(button)

    def _create_radio_buttons(self):
        dict_radio_button = {
            "КРС": [True, "bos taurus"],
            "Овцы": [False, "sheep"],
            "Олени": [False, "deer"],
        }
        self.list_radio_button = []
        for name, data in dict_radio_button.items():
            radio_button = QRadioButton(name)
            radio_button.species = data[1]
            radio_button.setChecked(data[0])
            radio_button.toggled.connect(self._on_radio_button_clicked)
            self.list_radio_button.append(radio_button)

    def _create_check_box(self):
        self.list_check_box = [QCheckBox(text="Подбирать матерей?")]

    def _on_radio_button_clicked(self):
        rb = self.sender()
        if rb.isChecked():
            self.species_animal = rb.species
            self.combobox.clear()
            self.get_farms()
            self.combobox.addItems(
                self.list_farms
            )

    def get_farms(self):
        set_farms = self.manager_db.get_farms(
            self.select_model(self.species_animal)
        )
        self.list_farms = list(map(str, set_farms))

    def _create_combo_box(self):
        self.get_farms()
        self.combobox = QComboBox()
        self.combobox.addItems(self.list_farms)
        self.combobox.currentTextChanged.connect(self.set_farm)

    def open_file_invertory(self):
        self.path_invertory = QFileDialog.getOpenFileName(
            None,
            "Открыть опись",
            "",
            'CSV (*.csv);; Text Files (*.txt);; Excel (*.xlsx)'
        )[0]

    def open_file_profils(self):
        self.path_profils = QFileDialog.getOpenFileName(
            None,
            "Открыть данные по генотипам",
            "",
            'CSV (*.csv);; Text Files (*.txt);; Excel (*.xlsx)'
        )[0]

    def open_table_invertory(self):
        self.table = TableInputData(self)
        self.table.show()

    def open_table_profils(self):
        model = self.select_model(self.species_animal)
        self.table = TableInputData(self)
        self.table.show()

    def select_model(self, species: str):
        dict_models = {
            "bos taurus": Cow,
            "deer": Deer,
            "sheep": Sheep,
        }
        return dict_models.get(species, Cow)

    def set_farm(self, text):
        print(text)
        self.farm = text

    def start_pipline_gen_password(self):
        model = self.select_model(self.species_animal)
        print()
        print(self.list_check_box[0].isChecked())
        self.manager_ms = ManagerDataMS(model)


class TableInputData(QDialog):
    """Окно для для ввода данных по потомку."""
    """
        Описание

        Параметры:
        ----------
        Возвращает:
        -------
        """
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.model = QStandardItemModel(19, 1)
        self.tableView = QTableView()
        header_labels = ['Потомок']
        self.model.setHorizontalHeaderLabels(header_labels)
        self.header_labels_vertical = ["x" for _ in range(19)]
        self.model.setVerticalHeaderLabels(self.header_labels_vertical)
        self.tableView.setModel(self.model)
        self.tableView.installEventFilter(self)
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.tableView)

        self.pushButton = QPushButton(self)
        self.pushButton.clicked.connect(self._close)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self._save_data)
        self.pushButton.setText("Закрыть окно")

        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.pushButton)

        self.table_wiew = None

    def _save_data(self):
        pass

    def _close(self):
        pass


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
