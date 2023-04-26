from PyQt5.QtCore import Qt, QTimer, QObject, QThread, pyqtSignal, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QKeySequence
from PyQt5.QtWidgets import (
    QWidget, QToolBar, QGridLayout, QDialog, QMenuBar, QMenu, QFileDialog,
    QLabel, QMainWindow, QMessageBox, QLineEdit, QTextEdit, QTableView,
    QSplashScreen, QTableWidget, QPushButton, QAction, QComboBox,
    QVBoxLayout, QRadioButton, QButtonGroup, QCheckBox, QApplication
)
import pandas as pd
import threading
from .managers import ManagerDataMS, ManagerDB, ManagerFile
from .models import  Cow, Deer, Sheep, Farm
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
        self.manager_file = ManagerFile()
        self.data_invertory = None
        self.data_profils = None
        self.link_to_data = {"invertory": None, "profils": None}

        super().__init__(statusbar, *args, **kwargs)

        self.set_farm()

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
            self.select_model()
        )
        self.list_farms = list(map(str, set_farms))

    def _create_combo_box(self):
        self.get_farms()
        self.combobox = QComboBox()
        self.combobox.addItems(self.list_farms)
        self.combobox.currentTextChanged.connect(self.set_farm)

    def open_file_invertory(self):
        self.path_invertory = self.manager_file.save_path_for_file_to_open(
            "Открыть данные по описи"
        )
        self.link_to_data["invertory"] = self.manager_file.read_file()

    def open_file_profils(self):
        self.path_profils = self.manager_file.save_path_for_file_to_open(
            "Открыть данные по генотипам"
        )
        self.link_to_data["profils"] = self.manager_file.read_file()

    def open_table_invertory(self):
        model = self.select_model()
        fields_to_header = model.get_filds()
        self.table_invertory = TableInputData(
            self, "invertory", fields_to_header
        )
        self.table_invertory.show()

    def open_table_profils(self):
        model = self.select_model()
        fields_to_header = model.get_filds()
        self.table_profils = TableInputData(
            self, "profils", fields_to_header, None, False
        )
        self.table_profils.show()

    def select_model(self):
        dict_models = {
            "bos taurus": Cow,
            "deer": Deer,
            "sheep": Sheep,
        }
        return dict_models.get(self.species_animal, Cow)

    def set_farm(self, text=None):
        if text is None:
            text = self.combobox.textActivated
        self.farm = self.manager_db.get_farm(text, self.species_animal)

    def start_pipline_gen_password(self):
        model = self.select_model()
        self.manager_ms = ManagerDataMS(self.farm, model)
        self.manager_ms.set_data_invertory(self.link_to_data["invertory"])
        self.manager_ms.set_data_profils(self.link_to_data["profils"])
        path = self.manager_file.save_path_file_for_pass()
        self.manager_ms.pipline_creat_doc_pas_gen(path)


class TableInputData(QDialog):
    """Окно для для ввода данных по потомку."""
    def __init__(
            self, parent, link,
            header_labels: list = None,
            index_labels: list = None, is_invertory: bool = True,
            is_ms_prof: bool = True
            ):
        super().__init__(parent=parent)
        self.link = link
        self.parent_out = parent
        self.header_labels: list = header_labels
        self.index_labels: list = index_labels
        self.is_invertory: bool = is_invertory
        self.is_ms_prof: bool = is_ms_prof
        self.index = []
        self.columns = []
        self.clipboard = []
        self._create_layout()

    def get_data(self):
        return self.data

    def _create_layout(self):
        self._create_button()
        self._create_table()
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.table_wiew)
        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.close_button)

    def _create_table(self):
        self.model = QStandardItemModel(19, 1)
        self.table_wiew = QTableView()
        if self.is_invertory:
            self.columns = [
                "Инвентарный номер", "Кличка", "Номер пробы",
                "Инв. № предка - М", "Кличка предка - М",
                "Инв. № предка - О", "Кличка предка - О",
            ]
            self.model.setHorizontalHeaderLabels(
                self.columns
            )
        elif self.is_ms_prof and self.header_labels is None:
            self.columns = [str(x) for x in range(300)] 
            self.model.setHorizontalHeaderLabels(self.columns)
        elif self.is_ms_prof and self.header_labels is not None:
            locus_1 = list(map(lambda x: x + "_1", self.header_labels[4:]))
            locus_2 = list(map(lambda x: x + "_2", self.header_labels[4:]))
            header = ["Sample Name"]
            for i in range(len(locus_1)):
                header.append(locus_1[i])
                header.append(locus_2[i])
            self.columns = header
            self.model.setHorizontalHeaderLabels(self.columns)
        else:
            self.columns = ["Потомок"]
            self.model.setHorizontalHeaderLabels(self.columns)

        if self.is_ms_prof and self.index_labels is None:
            self.index = [str(x) for x in range(300)]
            self.model.setVerticalHeaderLabels(self.index)
        elif self.is_ms_prof and self.index_labels is not None:
            self.index = self.index_labels
            self.model.setVerticalHeaderLabels(self.index)
        else:
            self.index = self.index_labels
            self.model.setVerticalHeaderLabels(self.header_labels[4:])
        self.table_wiew.setModel(self.model)
        self.table_wiew.installEventFilter(self)

    def _create_button(self):
        self.close_button = QPushButton("Закрыть окно", self)
        self.close_button.clicked.connect(self._close)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self._save_data)

    def get_data_from_table(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                try:
                    self.data.iloc[row, col] = self.model.item(row, col).text()
                except AttributeError:
                    pass
        self.parent_out.link_to_data[self.link] = self.data

    def _save_data(self):
        rows = self.model.rowCount()
        cols = self.model.columnCount()
        self.data = pd.DataFrame(
            columns=self.columns,
            index=self.index
        )
        thred = threading.Thread(
            target=self.get_data_from_table, args=(rows, cols)
        )
        thred.start()

    def _copy(self):
        self.clipboard.clear()
        selected = self.table_wiew.selectedIndexes()
        rows = []
        columns = []
        for index in selected:
            rows.append(index.row())
            columns.append(index.column())
        min_row = min(rows)
        min_col = min(columns)
        max_col = max(columns)
        data = []
        res_clipboard = []
        for index in selected:
            if index.column() == max_col:
                res_clipboard.append(
                    (
                        index.row() - min_row,
                        index.column() - min_col,
                        index.data()
                    )
                )
                data.append(res_clipboard)
                res_clipboard = []
            else:
                res_clipboard.append(
                    (
                        index.row() - min_row,
                        index.column() - min_col,
                        index.data()
                    )
                )
        res_str = ''
        for value_row in data:
            flag = True
            for val in value_row:
                value = " " if val[2] is None else val[2]
                if flag:
                    res_str += f'{value}'
                    flag = False
                else:
                    res_str += f'\t{value}'
            res_str += "\n"
        clipboard = QApplication.clipboard()
        clipboard.setText(res_str)

    def _paste(self):
        table = QApplication.clipboard()
        mime = table.mimeData()
        data = mime.data('text/plain')

        data = str(data.data(), 'cp1251')[0:]
        data = data.split('\n')
        columns = data[0].split(';')
        columns[0] = columns[0].replace("'", "")
        self.data_paste = pd.DataFrame(
            columns=columns,
            index=[x for x in range(len(data))]
        )
        for i in range(0, len(data)-1):
            data_in = data[i].split(';')
            for j in range(len(data_in)):
                self.data_paste.iloc[i, j] = data_in[j]
        self.data_paste = self.data_paste.dropna(how='all')
        self.data_paste = self.data_paste.dropna(how='all', axis='columns')
        current = self.table_wiew.currentIndex()
        if not current.isValid():
            current = self.model.index(0, 0)

        first_row = current.row()
        first_column = current.column()
        selection = self.table_wiew.selectionModel()

        for row in range(len(self.df)):
            for column in range(len(self.data_paste.columns)):
                data_o = self.data_paste.iloc[row, column]
                index = self.model.index(
                    first_row + row, first_column + column
                )
                self.model.setData(index, data_o, Qt.DisplayRole)
                selection.select(index, selection.Select)
        self.table_wiew.setSelectionModel(selection)

    def _close(self):
        self.close()

    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            if event == QKeySequence.Copy:
                self._copy()
                return True
            elif event == QKeySequence.Paste:
                self._paste()
                return True
        elif event.type() == QEvent.ContextMenu:
            menu = QMenu()
            copy_action = menu.addAction('Copy')
            copy_action.triggered.connect(self._copy)
            paste_action = menu.addAction('Paste')
            paste_action.triggered.connect(self._paste)

            if not self.table_wiew.selectedIndexes():
                copy_action.setEnabled(False)
                paste_action.setEnabled(False)
            if not self.clipboard:
                paste_action.setEnabled(False)
            menu.exec(event.globalPos())
            return True
        return super(TableInputData, self).eventFilter(source, event)


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

