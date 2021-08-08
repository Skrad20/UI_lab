#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pprint import pprint
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from numpy import e
from pandas.core.frame import DataFrame
from func.func_ms import *
from func.func_issr import *
from peewee import *
import datetime as dt
import functools


adres_job = ''


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
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
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
        self.button_1.setText(label_first)
        self.button_1.clicked.connect(func_first)
        self.button_2 = QPushButton()
        self.button_2.setText(label_second)
        self.button_2.clicked.connect(func_second)
        self.button_1.setMinimumHeight(100)
        self.button_2.setMinimumHeight(100)
        self.button_layout.addWidget(self.button_1)
        self.button_layout.addWidget(self.button_2)
        self.vb.addLayout(self.button_layout)

    def label_creat(self, label_str: str, class_func = None) -> None:
        """Создает надпись в окне программы."""
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(label_str)
        self.label.setWordWrap(True)
        self.vb.addWidget(self.label)

    def fill_table_aus_base(self, class_func = None) -> None:
        """Заполняет таблицу из базы."""
        pass

    def fill_table_hand(self, class_func = None) -> None:
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


class WindowTabl(MainDialog):
    """Окно с табличкой"""
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.tabl = table
        self.vl = QVBoxLayout(self)
        self.pushButton = QPushButton(self)
        self.pushButton_res = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
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
        self.pushButton.setObjectName("pushButton")
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
        
        self.hosbut_all = {}
        text_2 = 'Выберите хозяйства'
        labe_text_2 = QLabel(text_2)
        labe_text_2.setAlignment(Qt.AlignCenter)
        self.vb.addWidget(labe_text_2)
        hosbut = [
            'Гледенское',
            'Родина',
            'Двина',
            'Погореловское',
            'Присухронское',
            'Выбрать всех',
        ]
        hosbut_chek = {}
        for name in hosbut:
            hosbut_chek[name] = QCheckBox(name, self)
            hosbut_chek[name].stateChanged.connect(lambda checked, res = name: self.check_answer(checked, res))
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
        button_oprn_file = QPushButton()
        button_oprn_file.setText('Открыть файл CSV')
        button_oprn_file.clicked.connect(self.open_file_result)
        try:
            df = search_father(self.adres, self.hosbut_all)
            self.table_wiew = ResOut(df)
            dialog = WindowResulWiew(
                self.table_wiew,
                'Biotech Lab: Результаты анализа',
                button_oprn_file,
                '',
                self
            )
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'Вы выбрали неверные данные:\n {e}')


class WindowGenPassWord(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)
        self.adres_invertory = r''
        self.adres_genotyping = r''
        self.df_error = pd.DataFrame()
        self.len_df = 0

    def gen_password_invertory(self) -> None:
        """Генерирует запись о добавленых данных"""
        self.adres_invertory = enter_adres('Добавить опись')
        if self.adres_invertory != '':
            self.label_creat('Данные по описи добавлены')

    def gen_password_genotyping(self) -> None:
        """Генерирует запись о добавленых данных"""
        self.adres_genotyping = enter_adres('Добавить данные по генотипированию')
        if self.adres_genotyping != '':
            self.label_creat('Данные по генотипированию добавлены')

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
        except  Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'Вы выбрали неверные данные:\n {e}')


class WindowAbout(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)


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
        self.res_df_issr = issr_analit_func(self.adres_issr_in)
        try:
            self.res_df_issr = issr_analit_func(self.adres_issr_in)
            self.adres_res = save_file(self.res_df_issr)
            self.label_creat(str(dt.datetime.now()))
            self.button_creat(self.open_file_result, 'Открыть файл с результатами')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка ввода', f'Вы выбрали неверные данные:\n {e}')


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
            QMessageBox.information(self, 'Ошибка ввода', f'Вы выбрали неверные данные: \n {e}')


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


class WindowTableEnterData(MainDialog):
    """Окно для для ввода даннных."""
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.vl = QVBoxLayout(self)
        self.pushButton = QPushButton(self)
        self.pushButton_res = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.botton_closed)
        self.save_button = QPushButton("Заполнить ячейки", self)
        self.save_button.clicked.connect(self.get_data)
        self.pushButton.setText("Закрыть окно")
        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.pushButton)
        self.table_wiew = None

    def on_fill(self):
        self.table.setRowCount(int(self.spin.text()))
        self.get_data()

    def get_data(self):
        if self.table_wiew != None:
            self.vl.removeWidget(self.table_wiew)
            self.vl.removeWidget(self.save_button_end)
        table = QApplication.clipboard()
        mime = table.mimeData()
        data = mime.data('application/x-qt-windows-mime;value="Csv"')
        data = str(data.data())[1:]
        data = data.split(r'\r\n')
        columns = data[0].split(';')
        columns[0] = columns[0].replace("'", "")
        self.df = pd.DataFrame(columns=columns, index=[x for x in range(len(data))])
        for i in range(1, len(data)-1):
            data_in = data[i].split(';')
            for j in range(len(data_in)):
                self.df.iloc[i-1, j] = data_in[j]
        self.out_data()
    
    def out_data(self):
        self.table_wiew = ResOut(self.df)
        self.vl.addWidget(self.table_wiew)
        self.save_button_end = QPushButton("Сохранить данные", self)
        self.save_button_end.clicked.connect(self.save_data)
        self.vl.addWidget(self.save_button_end)

    def save_data(self):
        self.df_res = DataFrame(columns=self.df.columns, index = self.df.index)
        for i in range(self.table_wiew.rowCount()):
            for j in range(self.table_wiew.columnCount()):
                    if self.table_wiew.item(i,j).text() != 'nan':
                        self.df_res.iloc[i, j] = self.table_wiew.item(i,j).text()
        self.df_res = self.df_res.dropna(how='all')
        print(self.df_res)


class WindowTest(Window_main):
    """Окно для тестирования функций."""
    def __init__(self, name: str):
        super().__init__(name)
        
    def show_enter_data_tabl(self):
        dialog = WindowTableEnterData(None, 'Biotech Lab: example genotyping', self)
        dialog.exec_()


class GeneralWindow(QMainWindow):
    """Управляет окнами программы."""
    def __init__(self) -> None:
        super(GeneralWindow, self).__init__()
        self.setWindowTitle('MainWindow')
        
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
        text = 'Добро пожаловать!\n Здесь Вы найдёте методы, которые помогут Вам в анализе данных получаемых в лаборатории.'
        self.window.label_creat(text)
        self.window.button_creat(self.show_window_MS,'Микросателлитный анализ')
        self.window.button_creat(self.show_window_ISSR, 'Анализ ISSR')
        self.window.button_creat(self.show_about_programm, 'О программе')
        self.window.button_creat(self.show_window_tests, 'Тест')
        self.window.show()

    def show_window_tests(self):
        """Окно для тестирования новых функций"""
        try:
            self.window = WindowTest('Biothech Lab: testing')
            
            self.window.button_creat(self.window.show_enter_data_tabl, 'Открыть окно для ввода информации')
            self.window.button_creat(self.show_window_biotech, 'На главную')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка выполнения:\n {e}')

    def show_window_MS(self) -> None:
        """Отрисовывает окно анализа микросателлитов."""
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

    def show_window_MS_aus_word(self) -> None:
        '''Отрисовывает окно отбора данных из  Word.'''
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

    def show_window_MS_serch_father(self) -> None:
        '''Отрисовывает окно поиска отцов.'''
        self.window = WindowSearchFarher('Biotech Lab: Microsatellite analysis. Search father')
        global adres_job
        adres_job = r'func\data\search_fatherh\bus_search.csv'
        self.window.button_creat(self.window.res_search_cow_father, 'Выбрать файл с данными о потомке')
        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()

    def show_creat_pass_doc_gen(self) -> None:
        '''Отрисовывает окно генерации паспортов.'''
        self.window = WindowGenPassWord('Biotech Lab: Microsatellite analysis. Generation password')
        text_1 = 'Собрать паспорта по описи и результатам генотипирования'
        self.window.label_creat(text_1)
        global adres_job
        adres_job = r'func\data\creat_pass_doc\combined_file.docx'
        self.window.button_creat_double(
            self.window.gen_password_invertory, 'Выбрать опись',
            self.window.example_inventiry, 'Пример'
        )
        self.window.button_creat_double(
            self.window.gen_password_genotyping, 'Результаты\nгенотипирования',
            self.window.example_genotyping, r'Пример'
        )
        self.window.button_creat(self.window.gen_password, 'Обработать')
        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()

    def show_about_programm(self):
        '''Отрисовывает окно о программе.'''
        self.window = WindowAbout('Biotech Lab: about programm')
        text_1 = (
            'Версия 1.0.0\n\nТехнологии: Python 3.7.0, Qt, Pandas, \nNumpy, Peewee, GitHub\n' +
            '\nГод разработки: 2021'
        )
        pixmap = QPixmap(r'data/nii.jpg')
        self.window.label = QLabel(self)
        self.window.label.setPixmap(pixmap)
        self.window.label.resize(pixmap.width(), pixmap.height())
        self.window.label.setAlignment(Qt.AlignCenter)
        self.window.resize(pixmap.width(), pixmap.height())
        self.window.vb.addWidget(self.window.label)
        self.window.label_creat(text_1)
        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()

    def show_window_ISSR(self) -> None:
        """Отрисовывает окно ISSR."""
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
    
    def open_file(self) -> None:
        """Сохраняет путь к файлу"""
        self.file_adres = QFileDialog.getOpenFileName(self, 
                        'Open File', 
                        './', 
                        'Text Files (*.txt);; CSV (*.csv')[0]
    
    def __repr__(self) -> str:
        return  f'Переменные: {self.file_adres}'
