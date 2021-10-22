#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime as dt
from pprint import pprint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pandas.core.frame import DataFrame
from func.func_answer_error import answer_error
from func.func_ms import *
from func.func_issr import *
from peewee import *
from classes.class_bar import Progress_diaog


adres_job = ''
data_job = ''
adres_job_search_father= ''


class Window_main(QWidget):
    """Рабочее окно программы."""
    def __init__(self, name: str):
        super(Window_main, self).__init__()
        self.name = name
        self.initUI(name)
        self.adres_res = ''
        self.vb = QVBoxLayout(self)
        self.db = SqliteDatabase('db.sqlite3')

    def initUI(self, name):
        """Конструктор формы"""
        self.center()
        self.setMinimumWidth(400)
        self.setMinimumHeight(550)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data\icon.ico'))
        self.show()

    def center(self):
        """Центрирует окно"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_creat(self, func, label: str, class_func = None) -> None:
        """Создает кнопку в окне программы."""
        self.button = QPushButton()
        self.button.setText(label)
        self.button.clicked.connect(func)
        self.vb.addWidget(self.button)

    def button_creat_double(self, func_first, label_first: str, func_second, label_second: str, class_func = None) -> None:
        """Создает 2 кнопки в ряд в окне программы."""
        self.button_layout = QHBoxLayout()
        self.button_1 = QPushButton()
        self.button_1.setObjectName('first_button_2')
        self.button_1.setText(label_first)
        self.button_1.clicked.connect(func_first)
        self.button_2 = QPushButton()
        self.button_1.setObjectName('second_button_2')
        self.button_2.setText(label_second)
        self.button_2.clicked.connect(func_second)
        self.button_1.setMinimumHeight(100)
        self.button_2.setMinimumHeight(100)
        self.button_layout.addWidget(self.button_1)
        self.button_layout.addWidget(self.button_2)
        self.vb.addLayout(self.button_layout)

    def label_creat(self, label_str: str, class_func=None) -> None:
        """Создает надпись в окне программы."""
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(label_str)
        self.label.setWordWrap(True)
        self.vb.addWidget(self.label)

    def fill_table_aus_base(self, class_func=None) -> None:
        """Заполняет таблицу из базы."""
        pass

    def fill_table_hand(self, class_func=None) -> None:
        """Заполняет таблицу из вставки. Передает в базу."""
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(20)
        self.vb.addWidget(self.table)

    def open_file_result(self) -> None:
        '''Открывает файл по адресу, сохраняемому в глобальной переменной'''
        os.startfile(adres_job)

    def open_file_result_self(self) -> None:
        '''Открывает файл по адресу, сохраняемому в переменной класса'''
        os.startfile(self.adres_res)

    def __repr__(self) -> str:
        """"""
        return self.name


class MainDialog(QDialog):
    """Окно доп вывода"""
    def __init__(self, table, name, parent=None):
        super(MainDialog, self).__init__(parent)
        self.initUI(name)
        self.tabl = table

    def botton_closed(self):
        self.close()

    def initUI(self, name):
        """Конструктор формы"""
        self.center()
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data\icon.ico'))
        self.show()

    def center(self):
        """Центрирует окно"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().topLeft()
        qr.moveCenter(cp)
        self.move(qr.center())
        self.clipboard = []

    def eventFilter(self, source, event):
        '''Отслеживание событий вставки или копирования.'''
        try:
            if event.type() == QEvent.KeyPress:
                if event == QKeySequence.Copy:
                    self.copySelection()
                    return True
                elif event == QKeySequence.Paste:
                    self.pasteSelection()
                    return True

            elif event.type() == QEvent.ContextMenu:
                menu = QMenu()
                copyAction = menu.addAction('Copy')
                copyAction.triggered.connect(self.copySelection)
                pasteAction = menu.addAction('Paste')
                pasteAction.triggered.connect(self.pasteSelection)
                if not self.tableView.selectedIndexes():
                    copyAction.setEnabled(False)
                    pasteAction.setEnabled(False)
                if not self.clipboard:
                    pasteAction.setEnabled(False)
                menu.exec(event.globalPos())
                return True
            return super(MainDialog, self).eventFilter(source, event)
        except Exception as e:
            QMessageBox.critical(self, 'Что-то пошло не так', f'{answer_error()} Подробности:\n {e}')

    def copySelection(self):
        '''Копирование данных ctrl+С.'''
        self.clipboard.clear()
        selected = self.tableView.selectedIndexes()
        rows = []
        columns = []
        for index in selected:
            rows.append(index.row())
            columns.append(index.column())
        minRow = min(rows)
        minCol = min(columns)
        for index in selected:
            self.clipboard.append((index.row() - minRow, index.column() - minCol, index.data()))
        df_in = pd.DataFrame(columns=[x for x in range(300)], index=[x for x in range(50)])
        for i in range(len(self.clipboard)):
            data_copy = self.clipboard[i]
            row = data_copy[0]
            col = data_copy[1]
            data_in_df = data_copy[2]
            df_in.iloc[row, col] = data_in_df
        df_in = df_in.dropna(how='all')
        df_in = df_in.dropna(how='all', axis='columns')

    def pasteSelection(self):
        '''Вставка данных ctrl+V.'''
        table = QApplication.clipboard()
        mime = table.mimeData()
        #data = mime.data('application/x-qt-windows-mime;value="Csv"')
        data = mime.data('text/plain')

        data = str(data.data(), 'cp1251')[0:]
        data = data.split('\n')
        print(data)
        columns = data[0].split(';')
        columns[0] = columns[0].replace("'", "")
        self.df = pd.DataFrame(
            columns=columns,
            index=[x for x in range(len(data))]
        )
        for i in range(0, len(data)-1):
            data_in = data[i].split(';')
            for j in range(len(data_in)):
                print(str(data_in[j]))
                self.df.iloc[i, j] = data_in[j]
        self.df = self.df.dropna(how='all')
        self.df = self.df.dropna(how='all', axis='columns')
        current = self.tableView.currentIndex()
        if not current.isValid():
            current = self.model.index(0, 0)

        firstRow = current.row()
        firstColumn = current.column()
        selection = self.tableView.selectionModel()

        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                row = i
                column = j
                data_o = self.df.iloc[row, column]
                index = self.model.index(firstRow + row, firstColumn + column)
                self.model.setData(index, data_o, Qt.DisplayRole)
                selection.select(index, selection.Select)

        self.tableView.setSelectionModel(selection)


class WindowTabl(MainDialog):
    """Окно с табличкой"""
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.tabl = table
        self.vl = QVBoxLayout(self)
        self.pushButton = QPushButton(self)
        self.pushButton_res = QPushButton(self)
        self.pushButton.clicked.connect(self.botton_closed)
        self.vl.addWidget(self.tabl)
        self.vl.addWidget(self.pushButton)
        self.pushButton.setText("Закрыть окно")


class WindowResulWiew(MainDialog):
    '''Рабочее окно для вывода результатов'''
    def __init__(self, table, name, button, label, parent):
        super().__init__(table, name, parent=parent)
        self.tabl = table
        self.button = button
        self.vl = QVBoxLayout(self)
        self.pushButton = QPushButton(self)
        self.pushButton.clicked.connect(self.botton_closed)
        self.label_start = QLabel(label)
        self.label_date = QLabel(str(dt.datetime.now()))
        self.vl.addWidget(self.label_date)
        self.vl.addWidget(self.label_start)
        self.vl.addWidget(self.tabl)
        self.vl.addWidget(self.button)
        self.vl.addWidget(self.pushButton)
        self.pushButton.setText("Закрыть окно")


class WindowSearchFarher(Window_main):
    '''Рабочее окно для поиска возможных отцов.'''
    def __init__(self, name: str):
        super().__init__(name)
        self.hosbut_all = {
            'Выбрать всех': False
        }
        text_2 = 'Выберите хозяйства'
        labe_text_2 = QLabel(text_2)
        labe_text_2.setAlignment(Qt.AlignCenter)
        self.vb.addWidget(labe_text_2)
        hosbut = [
            'Устюгмолоко',
            'Присухонское',
            'Заря',
            'Выбрать всех',
        ]
        hosbut_chek = {
        }
        for name in hosbut:
            hosbut_chek[name] = QCheckBox(name, self)
            hosbut_chek[name].stateChanged.connect(lambda checked, res=name: self.check_answer(checked, res))
        cp_layout1 = QGridLayout()
        j = 0
        x = 0
        for i in range(len(hosbut)):
            item = hosbut_chek[hosbut[i]]
            cp_layout1.addWidget(item, j, x)
            x += 1
            if x > 2:
                x = 0
                j += 1
        self.vb.addLayout(cp_layout1)
        text_1 = 'Подобрать отцов из выбранных хозяйств'
        labe_text = QLabel(text_1)
        labe_text.setAlignment(Qt.AlignCenter)
        self.vb.addWidget(labe_text)

    def check_answer(self, state, res='s'):
        if state == Qt.Checked:
            self.hosbut_all[res] = True
            print(self.hosbut_all)
        else:
            self.hosbut_all[res] = False
            print(self.hosbut_all)

    def res_search_cow_father(self, class_func = None) -> None:
        '''Вызывает функции анализа и поиска отцов'''
        self.adres = enter_adres()
        self.button_oprn_file = QPushButton()
        self.button_oprn_file.setText('Открыть файл CSV')
        self.button_oprn_file.clicked.connect(self.open_file_result)

        try:
            df = search_father(self.adres, self.hosbut_all)
            self.table_wiew = ResOut(df)
            dialog = WindowResulWiew(
                self.table_wiew,
                'Biotech Lab: Результаты анализа',
                self.button_oprn_file,
                '',
                self
            )
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'{answer_error()} Подробности:\n {e}')

    def data_result_in(self):
        self.window = WindowTableEnterDataSF(None, 'Biotech Lab: enter data', self.hosbut_all, self)
        self.window.show()
        self.window.exec_()


class WindowGenPassWord(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)
        self.adres_invertory = r''
        self.adres_genotyping = r''
        self.df_error = pd.DataFrame()
        self.len_df = 0
        text_1 = 'Собрать паспорта по описи и результатам генотипирования'
        self.label_creat(text_1)
        global adres_job
        adres_job = r'func\data\creat_pass_doc\combined_file.docx'
        self.button_layout = QHBoxLayout()
        self.button_1 = QPushButton()
        self.button_1.setText('Выбрать опись')
        self.button_1.clicked.connect(self.gen_password_invertory)
        self.button_2 = QPushButton()
        self.button_2.setText('Пример')
        self.button_2.clicked.connect(self.example_inventiry)
        self.button_1.setMinimumHeight(100)
        self.button_2.setMinimumHeight(100)
        self.button_layout.addWidget(self.button_1)
        self.button_layout.addWidget(self.button_2)
        self.vb.addLayout(self.button_layout)

        self.button_layout_2 = QHBoxLayout()
        self.button_3 = QPushButton()
        self.button_3.setText('Результаты\nгенотипирования')
        self.button_3.clicked.connect(self.gen_password_genotyping)
        self.button_4 = QPushButton()
        self.button_4.setText('Пример')
        self.button_4.clicked.connect(self.example_genotyping)
        self.button_3.setMinimumHeight(100)
        self.button_4.setMinimumHeight(100)
        self.button_layout_2.addWidget(self.button_3)
        self.button_layout_2.addWidget(self.button_4)
        self.vb.addLayout(self.button_layout_2)

        self.button_layout_3 = QHBoxLayout()
        self.button_5 = QPushButton()
        self.button_5.setText('Ввести данные\nописей')
        self.button_5.clicked.connect(self.add_data_in_table_invertory)
        self.button_6 = QPushButton()
        self.button_6.setText('Ввести данные\nпрофилей')
        self.button_6.clicked.connect(self.add_data_in_table_profils)
        self.button_5.setMinimumHeight(100)
        self.button_6.setMinimumHeight(100)
        self.button_layout_3.addWidget(self.button_5)
        self.button_layout_3.addWidget(self.button_6)
        self.vb.addLayout(self.button_layout_3)
        self.button_creat(self.gen_password, 'Обработать')

    def gen_password_invertory(self) -> None:
        """Генерирует запись о добавленых данных"""
        self.adres_invertory = enter_adres('Добавить опись')
        if self.adres_invertory != '':
            #self.label_creat('Данные по описи добавлены')
            self.button_1.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
                )
            )

    def add_data_in_table_invertory(self) -> None:
        '''Выводит окно для вставки данных описей в таблицу.'''
        self.adres_invertory = r'func\data\creat_pass_doc\inventory_aus_table.csv'
        try:
            self.window = Wind_Table_GP_invertory(None, 'Biotech Lab: enter data invertory', self)
            self.window.show()
            self.window.exec_()
            self.button_5.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
                )
            )
        except Exception as e:
            QMessageBox.critical(self, 'Что-то пошло не так', f'{answer_error()} Подробности:\n {e}')

    def add_data_in_table_profils(self) -> None:
        '''Выводит окно для вставки данных профилей в таблиц.'''
        try:
            self.adres_genotyping = r'func\data\creat_pass_doc\profils_aus_table.csv'
            self.window = Wind_Table_GP_profils(None, 'Biotech Lab: enter data invertory', self)
            self.window.show()
            self.window.exec_()
            self.button_6.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
                )
            )
        except Exception as e:
            QMessageBox.critical(self, 'Что-то пошло не так', f'{answer_error()} Подробности:\n {e}')

    def gen_password_genotyping(self) -> None:
        """Генерирует запись о добавленых данных"""
        self.adres_genotyping = enter_adres('Добавить данные по генотипированию')
        if self.adres_genotyping != '':
            #self.label_creat('Данные по генотипированию добавлены')
            self.button_3.setStyleSheet(
                    (
                    'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
                )
            )

    def gen_analit_password_creat(self) -> None:
        """Проводит анализ полученных данных"""
        self.hosbut = self.fenster_enter_date()
        self.adres_res = save_file_for_word('Сохранить результаты')
        self.df_error = creat_doc_pas_gen(
            self.adres_invertory,
            self.adres_genotyping,
            self.adres_res,
            self.hosbut,
        )
        self.len_df = len(self.df_error)

    def example_inventiry(self) -> None:
        '''Открывает файл пример для описи.'''
        df_example_inventiry = pd.read_csv(r'func\data\creat_pass_doc\inventory_example.csv', sep=';', decimal=',', encoding='cp1251')
        table_wiew = ResOut(df_example_inventiry)
        dialog = WindowTabl(table_wiew, 'Biotech Lab: example inventiry', self)
        dialog.exec_()

    def example_genotyping(self) -> None:
        '''Открывает файл пример для генотипирования.'''
        df_example_genotyping = pd.read_csv(r'func\data\creat_pass_doc\profils_example.csv', sep=';', decimal=',', encoding='cp1251')
        table_wiew = ResOut(df_example_genotyping)
        dialog = WindowTabl(table_wiew, 'Biotech Lab: example genotyping', self)
        dialog.exec_()

    def fenster_enter_date(self) -> str:
        '''Выводит окно ввода данных.'''
        dialog = Form('Введите название хозяйства')
        dialog.exec_()
        hosbut = dialog.button_click()
        return hosbut

    def gen_password(self) -> None:
        '''Вызывает функции генерации паспортов.'''
        button_oprn_file = QPushButton()
        button_oprn_file.setText('Открыть файл с паспортами')
        button_oprn_file.clicked.connect(self.open_file_result_self)
        try:
            self.gen_analit_password_creat()
            table_wiew = ResOut(self.df_error)
            len_df_res = self.len_df
            dialog = WindowResulWiew(
                table_wiew,
                'Biotech Lab: Результаты анализа',
                button_oprn_file,
                ('Количество ошибок ' + str(len_df_res)),
                self
            )
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'{answer_error()} Подробности:\n {e}')


class WindowAbout(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)
        self.initUI_self()

    def initUI_self(self):
        """Конструктор формы"""
        self.center()
        self.setMaximumWidth(500)
        self.setMaximumHeight(500)
        self.setWindowIcon(QIcon('data\icon.ico'))
        self.show()


class WindowISSR(Window_main):
    '''Рабочее окно для обработки ISSR.'''
    def __init__(self, name: str):
        super().__init__(name)

    def gen_issr(self) -> None:
        '''Ввод результатов ISSR'''
        self.adres_issr_in = enter_adres('Добавить данные по ISSR')
        if self.adres_issr_in != '':
            self.label_creat('Данные по ISSR добавлены')

    def example_issr(self) -> None:
        '''Вывод примера оформления'''
        df_example_inventiry = pd.read_csv(r'func\data\issr\issr.txt', sep='\t', decimal=',', encoding='cp1251')
        table_wiew = ResOut(df_example_inventiry)
        dialog = WindowTabl(table_wiew, 'Biotech Lab: example ISSR', self)
        dialog.exec_()

    def analis_issr(self) -> None:
        '''Анализ issr'''
        try:
            
            self.res_df_issr = issr_analit_func(self.adres_issr_in)
            self.res_df_issr = issr_analit_func(self.adres_issr_in)
            self.adres_res = save_file(self.res_df_issr)
            self.label_creat(str(dt.datetime.now()))
            self.button_creat(self.open_file_result, 'Открыть файл с результатами')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'{answer_error()} Подробности:\n {e}')


class WindowMSAusWord(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)

    def res_ms_aus_word_in_csv(self):
        '''Вызывает функции отбора данных из word'''
        self.label_creat(str(dt.datetime.now()))
        self.button_creat(self.open_file_result, 'Открыть файл CSV')
        self.adres = enter_adres('Выбрать документ')
        try:
            df = ms_out_word(self.adres)
            self.table_wiew = ResOut(df)
            self.vb.addWidget(self.table_wiew)
        except Exception as e:
            QMessageBox.information(self, 'Ошибка ввода', f'{answer_error()} Подробности:\n {e}')


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
        self.setWindowIcon(QIcon('data\icon.ico'))
        self.show()

    def center(self) -> None:
        """Центрирует окно"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().topLeft()
        qr.moveCenter(cp)
        self.move(qr.center())


class TableDataEnter(QTableWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:

            return
        super(TableDataEnter, self).keyPressEvent(event)


class WindowTableEnterDataSF(MainDialog):
    """Окно для для ввода даннных по потомку."""
    def __init__(self, table, name, hosbut_all, parent):
        super().__init__(table, name, parent=parent)
        self.hosbut_all = hosbut_all
        self.model = QStandardItemModel(19, 1)
        self.tableView = QTableView()
        header_labels = ['Потомок']
        self.model.setHorizontalHeaderLabels(header_labels)
        self.header_labels_vertical = [
            'BM1818',
            'BM1824',
            'BM2113',
            'CSRM60',
            'CSSM66',
            'CYP21',
            'ETH10',
            'ETH225',
            'ETH3',
            'ILSTS6',
            'INRA023',
            'RM067',
            'SPS115',
            'TGLA122',
            'TGLA126',
            'TGLA227',
            'TGLA53',
            'MGTG4B',
            'SPS113',
        ]
        self.model.setVerticalHeaderLabels(self.header_labels_vertical)
        self.tableView.setModel(self.model)
        self.tableView.installEventFilter(self)     
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.tableView)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.botton_closed)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_data)
        self.pushButton.setText("Закрыть окно")
        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.pushButton)
        self.table_wiew = None

    def save_data(self) -> None:
        '''Сохранение данных по потомкам.'''
        self.df_res = DataFrame(
            columns= [x for x in range(self.tableView.model().columnCount())], 
            index = [x for x in range(self.tableView.model().rowCount())])
        for i in range(self.tableView.model().rowCount()):
            for j in range(self.tableView.model().columnCount()):
                if self.tableView.model().index(i,j).data() != 'nan':
                    self.df_res.iloc[i, j] = self.tableView.model().index(i,j).data()
        self.df_res = self.df_res.dropna(how='all')
        data_job = self.df_res
        data_job.columns = ['Потомок']
        data_job['Локус'] = self.header_labels_vertical
        data_job = data_job[['Локус', 'Потомок']]
        data_job.to_csv(
            r'func\data\search_fatherh\bus_search_in_table.csv',
            sep=';',
            decimal=',',
            encoding='cp1251',
            index = False
        )
        global adres_job_search_father
        adres_job_search_father = r'func\data\search_fatherh\bus_search_in_table.csv'
        try:
            df = search_father(adres_job_search_father, self.hosbut_all)
            self.table_wiew = ResOut(df)
            dialog = WindowResulWiew(
                self.table_wiew,
                'Biotech Lab: Результаты анализа',
                None,
                '',
                self
            )
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'{answer_error()} Подробности:\n {e}')
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #004524);}' +
                'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
            )
        )


class Wind_Table_GP_invertory(MainDialog):
    '''Окно для ввода описи.'''
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.model = QStandardItemModel(150, 7)
        self.tableView = QTableView()
        self.header_labels = [
            'Инвентарный номер',
            'Кличка',
            'Номер пробы',
            'Инв.№ предка - M',
            'Кличка предка - M',
            'Инв.№ предка - O',
            'Кличка предка - O',
        ]
        self.model.setHorizontalHeaderLabels(self.header_labels)
        self.tableView.setModel(self.model)
        self.tableView.installEventFilter(self)     
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.tableView)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.botton_closed)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_data)
        self.pushButton.setText("Закрыть окно")
        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.pushButton)
        self.table_wiew = None

    def save_data(self) -> None:
        '''Cохранение данных по описи'''
        self.df_res = DataFrame(
            columns= [x for x in range(self.tableView.model().columnCount())], 
            index = [x for x in range(self.tableView.model().rowCount())])
        for i in range(self.tableView.model().rowCount()):
            for j in range(self.tableView.model().columnCount()):
                if self.tableView.model().index(i,j).data() != 'nan':
                    self.df_res.iloc[i, j] = self.tableView.model().index(i,j).data()
        self.df_res = self.df_res.dropna(how='all')
        data_job = self.df_res
        data_job.columns = self.header_labels
        data_job.to_csv(
            r'func\data\creat_pass_doc\inventory_aus_table.csv',
            sep=';',
            decimal=',',
            encoding='cp1251',
            index = False
        )
        self.adres_job_res = r'func\data\creat_pass_doc\inventory_aus_table.csv'
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b);}' +
                'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
            )
        )


class Wind_Table_GP_profils(MainDialog):
    '''Окно для ввода описи.'''
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.model = QStandardItemModel(150, 31)
        self.tableView = QTableView()
        self.header_labels = [
            'Sample Name',
            'Eth3 1',
            'Eth3 2',
            'Cssm66 1',
            'Cssm66 2',
            'inra23 1',
            'inra23 2',
            'BM1818 1',
            'BM1818 2',
            'ilsts6 1',
            'ilsts6 2',
            'Tgla227 1',
            'Tgla227 2',
            'Tgla126 1',
            'Tgla126 2',
            'Tgla122 1',
            'Tgla122 2',
            'Sps115 1',
            'Sps115 2',
            'Eth225 1',
            'Eth225 2',
            'Tgla53 1',
            'Tgla53 2',
            'Csrm60 1',
            'Csrm60 2',
            'Bm2113 1',
            'Bm2113 2',
            'Bm1824 1',
            'Bm1824 2',
            'Eth10 1',
            'Eth10 2',
        ]
        self.model.setHorizontalHeaderLabels(self.header_labels)
        self.tableView.setModel(self.model)
        self.tableView.installEventFilter(self)     
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.tableView)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.botton_closed)
        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_data)
        self.pushButton.setText("Закрыть окно")
        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.pushButton)
        self.table_wiew = None

    def save_data(self) -> None:
        '''Cохранение данных по описи'''
        self.df_res = DataFrame(
            columns= [x for x in range(self.tableView.model().columnCount())], 
            index = [x for x in range(self.tableView.model().rowCount())])
        for i in range(self.tableView.model().rowCount()):
            for j in range(self.tableView.model().columnCount()):
                if self.tableView.model().index(i,j).data() != 'nan':
                    self.df_res.iloc[i, j] = self.tableView.model().index(i,j).data()
        self.df_res = self.df_res.dropna(how='all')
        data_job = self.df_res
        data_job.columns = self.header_labels
        data_job.to_csv(
            r'func\data\creat_pass_doc\profils_aus_table.csv',
            sep=';',
            decimal=',',
            encoding='cp1251',
            index = False
        )
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #004524);}' +
                'QPushButton:hover {background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
            )
        )


class WindowTest(Window_main):
    """Окно для тестирования функций."""
    def __init__(self, name: str):
        super().__init__(name)

    def show_enter_data_tabl(self):
        dialog = Wind_Table_GP_invertory(None, 'Biotech Lab: example genotyping', self)
        dialog.exec_()

    def itiat_progress_bar(self):
        pr = Progress_diaog()
        progress = QProgressDialog("Copying files...", "Abort Copy", 0, 10, self)
        progress.setWindowModality()

        for i in range(10):
            progress.setValue(i)

            if progress.wasCanceled():
                break

        progress.setValue(10)


class GeneralWindow(QMainWindow):
    """Управляет окнами программы."""
    def __init__(self) -> None:
        super(GeneralWindow, self).__init__()
        self.setWindowTitle('MainWindow')
        self.setObjectName('General_window') 
        self.file_adres = ''
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

    def initUI(self):
        """Конструктор геометрии."""
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon(r'data\icon.jpg'))
        self.show()

    def show_window_biotech(self) -> None:
        """Отрисовывает окно биотеха."""
        self.window = Window_main('Biotech Lab')
        self.window.setObjectName('Biotech_window')
        text = 'Добро пожаловать!\n Здесь Вы найдёте методы, которые помогут Вам в анализе данных, получаемых в лаборатории.'
        self.window.label_creat(text)
        self.window.button_creat(self.show_window_MS,'Микросателлитный анализ')
        self.window.button_creat(self.show_window_ISSR, 'Анализ ISSR')
        self.window.button_creat(self.show_about_programm, 'О программе')
        self.window.button_creat(self.show_window_tests, 'Тест')
        self.window.show()

    def show_window_MS(self) -> None:
        """Отрисовывает окно анализа микросателлитов."""
        try:
            self.window = Window_main('Biotech Lab: Microsatellite analysis')
            text_1 = 'Подобрать отцов из имеющейся базы'
            self.window.label_creat(text_1)
            self.window.button_creat(self.show_window_MS_serch_father, 'Найти отца')
            text_2 = 'Собрать генетические паспорта животных'
            self.window.label_creat(text_2)
            self.window.button_creat(self.show_creat_pass_doc_gen, 'Собрать паспорта')
            text_3 = 'Выбрать данные из генетических паспортов'
            self.window.label_creat(text_3)
            self.window.button_creat(self.show_window_MS_aus_word, 'Собрать')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'{answer_error()} Подробности:\n {e}')

    def show_window_MS_aus_word(self) -> None:
        '''Отрисовывает окно отбора данных из  Word.'''
        try:
            self.window = WindowMSAusWord('Biotech Lab: Microsatellite analysis. Aus word')
            text_1 = 'Здесь можно выбрать данные из готовых генетических паспортов'
            self.window.label_creat(text_1)
            text_2 = (
                'Порядок действий: \n1) Данные из WORD нужно скопировать в EXCEL' + 
                '\n2) Из EXCEl скопировать в блокнот и сохранить' + 
                '\n3) Выбрать файл в программе и наслаждаться'
            )
            self.window.label_creat(text_2)
            global adres_job
            adres_job = r'func\data\ms_word\result_ms_word.csv'
            self.window.button_creat(self.window.res_ms_aus_word_in_csv, 'Выбрать файл с данными')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'{answer_error()} Подробности:\n {e}')

    def show_window_MS_serch_father(self) -> None:
        '''Отрисовывает окно поиска отцов.'''
        try:
            self.window = WindowSearchFarher('Biotech Lab: Microsatellite analysis. Search father')
            global adres_job
            adres_job = r'func\data\search_fatherh\bus_search.csv'
            self.window.button_creat(self.window.res_search_cow_father, 'Выбрать файл с данными о потомке')
            self.window.button_creat(self.window.data_result_in, 'Внести данные в таблицу')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'{answer_error()} Подробности:\n {e}')

    def show_creat_pass_doc_gen(self) -> None:
        '''Отрисовывает окно генерации паспортов.'''
        self.window = WindowGenPassWord('Biotech Lab: Microsatellite analysis. Generation password')
        self.window.setObjectName('WindowGenPassWord')
        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()

    def show_about_programm(self):
        '''Отрисовывает окно о программе.'''
        self.window = WindowAbout('Biotech Lab: about programm')
        self.window.setObjectName('WindowAbout')
        text_1 = (
            'Версия 1.0.1\n\nТехнологии: Python 3.7.0, Qt, Pandas, \nNumpy, Peewee, GitHub\n' +
            '\nГод разработки: 2021'
        )
        pixmap = QPixmap('data/nii.png')
        self.window.label = QLabel(self)
        self.window.label.setObjectName('JpgNii')
        self.window.label.setPixmap(pixmap)
        self.window.label.resize(pixmap.width(), pixmap.height())
        self.window.label.setAlignment(Qt.AlignCenter)
        self.window.resize(pixmap.width(), pixmap.height())
        self.window.vb.addWidget(self.window.label)
        self.window.label_creat(text_1)
        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()

    def show_window_ISSR(self) -> None:
        '''Отрисовывает окно ISSR.'''
        try:
            self.window = WindowISSR('Biotech Lab: ISSR analysis')
            text_1 = 'Здесь можно обработать первичные данные по ISSR'
            self.window.label_creat(text_1)
            self.window.button_creat_double(
                self.window.gen_issr, 'Результаты ISSR',
                self.window.example_issr, 'Пример'
            )
            self.window.button_creat(self.window.analis_issr, 'Обработать')
            self.window.button_creat(self.show_window_biotech, 'На главную')
            self.window.show()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'{answer_error()} Подробности:\n {e}')
    
    def tests_wiew(self) -> None:
        '''Запускает тестируемый код.'''
        dialog = WindowTableEnter('Biotech Lab: example inventiry', self)
        dialog.exec_()

    
    def open_file(self) -> None:
        """Сохраняет путь к файлу"""
        self.file_adres = QFileDialog.getOpenFileName(self, 
                        'Open File', 
                        './', 
                        'Text Files (*.txt);; CSV (*.csv')[0]
    def show_window_tests(self):
        """Окно для тестирования новых функций"""
        QMessageBox.critical(self, 'Что-то пошло не так', f'{answer_error()} Подробности:\n')
        try:
            self.window = WindowTest('Biothech Lab: testing')
            self.window.setStyleSheet('QWidget {background-color: blue;} QPushButton {background-color: green}')
            self.window.button_creat(self.window.show_enter_data_tabl, 'Открыть окно для ввода информации')
            self.window.button_creat(self.window.itiat_progress_bar, 'Прогресс бар')
            self.window.button_creat(self.show_window_biotech, 'На главную')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'{answer_error()} Подробности:\n {e}')
    
    def __repr__(self) -> str:
        return  f'Запуск успешен. Переменные среды: {self.file_adres}'
