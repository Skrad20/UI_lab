#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from func.func_ms import *
from peewee import *
import datetime as dt

adres_job = ''

class Window_main(QWidget):
    """Рабочее окно программы."""
    def __init__(self, name: str):
        super(Window_main, self).__init__()
        self.name = name
        self.setWindowTitle(name)
        self.setMinimumWidth(200)
        self.setMinimumHeight(200)
        self.vb = QVBoxLayout(self)
        self.db = SqliteDatabase('db.sqlite3')

    def button_creat(self, func, label: str, class_func = None) -> None:
        """Создает кнопку в окне программы."""
        self.button = QPushButton()
        self.button.setText(label)
        self.button.clicked.connect(func)
        self.vb.addWidget(self.button)
    
    def label_creat(self, label_str: str, class_func = None) -> None:
        """Создает надпись в окне программы."""
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText(label_str)
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

    def __repr__(self) -> str:
        """"""
        return self.name


class WindowSearchFarher(Window_main):
    '''Рабочее окно для поиска возможных отцов.'''
    def __init__(self, name: str):
        super().__init__(name)

    def res_search_cow_father(self, class_func = None) -> None:
        '''Вызывает функции анализа и поиска отцов'''
        self.label_creat(str(dt.datetime.now()))
        self.button_creat(self.open_file_result, 'Открыть файл CSV')
        self.adres = enter_adres()
        try:
            df = search_father(self.adres)
            self.table_wiew = ResOut(df)
            self.vb.addWidget(self.table_wiew)
        except:
            QMessageBox.information(self, 'Ошибка ввода', 'Вы выбрали неверные данные')


class WindowGenPassWord(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)

    def gen_password(self):
        '''Вызывает функции генерации паспортов'''
        self.label_creat(str(dt.datetime.now()))
        self.button_creat(self.open_file_result, 'Открыть файл CSV')
        self.adres = enter_adres()
        try:
            df = ms_out_word(self.adres)
            self.table_wiew = ResOut(df)
            self.vb.addWidget(self.table_wiew)
        except:
            QMessageBox.information(self, 'Ошибка ввода', 'Вы выбрали неверные данные')


class WindowAbout(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)



class WindowMSAusWord(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)
    
    def res_ms_aus_word_in_csv(self):
        '''Вызывает функции отбора данных из word'''
        self.label_creat(str(dt.datetime.now()))
        self.button_creat(self.open_file_result, 'Открыть файл CSV')
        self.adres = enter_adres()
        try:
            df = ms_out_word(self.adres)
            self.table_wiew = ResOut(df)
            self.vb.addWidget(self.table_wiew)
        except:
            QMessageBox.information(self, 'Ошибка ввода', 'Вы выбрали неверные данные')

class GeneralWindow(QMainWindow):
    """Управляет окнами программы."""
    def __init__(self) -> None:
        super(GeneralWindow, self).__init__()
        self.setWindowTitle('MainWindow')
        self.file_adres = ''
        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

    def show_window_biotech(self) -> None:
        """Отрисовывает окно биотеха."""
        self.window = Window_main('Biotech Lab')
        text = 'Добро пожаловать!\n Здесь вы найдёте методы, которые помогут вам в анализе данных получаемых в лаборатории.'
        self.window.label_creat(text)
        self.window.button_creat(self.show_window_MS,'Микросателлитный анализ')
        self.window.button_creat(self.show_window_ISSR, 'Анализ ISSR')
        self.window.button_creat(self.show_about_programm, 'О программе')
        
        self.window.show()

    def show_window_MS(self) -> None:
        """Отрисовывает окно анализа микросателлитов."""
        self.window = Window_main('Biotech Lab: Microsatellite analysis')
        text_1 = 'Подобрать отцов из имеющейся базы'
        self.window.label_creat(text_1)
        self.window.button_creat(self.show_window_MS_serch_father, 'Найти отца')
        text_2 = 'Собрать генетические паспорта животных'
        self.window.label_creat(text_2)
        self.window.button_creat(self.show_creat_pass_doc_gen, 'Собрать')
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
        text_1 = 'Подобрать отцов из имеющейся базы'
        self.window.label_creat(text_1)
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
        #adres_job = r'func\data\search_fatherh\bus_search.csv'

        #self.window.button_creat(self.window.res_search_cow_father, 'Выбрать файл с данными о потомке')

        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()
    
    def show_about_programm(self):
        '''Отрисовывает окно о программе.'''
        self.window = WindowAbout('Biotech Lab: about programm')
        text_1 = (
            'Версия 1.0.0\n\nТехнологии: Python 3.7.0, Qt, Pandas, \nNumpy, Peewee, GitHub\n' +
            '\nГод разработки: 2021'
        )
        self.window.label_creat(text_1)
        self.window.button_creat(self.show_window_biotech, 'На главную')
        self.window.show()

    def show_window_ISSR(self) -> None:
        """Отрисовывает окно ISSR."""
        self.window = Window_main('Biotech Lab: ISSR analysis')
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
