#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from .dialogs_classes import MainDialog
from pandas.core.frame import DataFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QMessageBox, QPushButton, QTableView,
                             QTableWidget, QVBoxLayout)

from func.db_job import save_bus_data_fater
from func.func_answer_error import answer_error
from lists_name.list_name_row import list_name_row_add_father
from code_app.models import BullFather


class TableAddFather(MainDialog):
    '''Окно для добавления отца.'''
    """
    Описание

    Параметры:
    ----------
    
    Возвращает:
    -------
    """
    def __init__(self, table, name, hosbut_all, parent):
        super().__init__(table, name, parent=parent)
        self.model = QStandardItemModel(22, 1)
        self.tableView = QTableView()
        header_labels = ['Профиль']
        self.model.setHorizontalHeaderLabels(header_labels)
        self.header_labels_vertical = list_name_row_add_father
        self.model.setVerticalHeaderLabels(self.header_labels_vertical)
        self.tableView.setModel(self.model)
        self.tableView.installEventFilter(self)
        self.vl = QVBoxLayout(self)
        self.vl.addWidget(self.tableView)
        self.pushButton = QPushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.botton_closed)
        self.save_button = QPushButton("Сохранить", self)
        try:
            self.save_button.clicked.connect(self.save_data)
        except Exception as e:
            name = '\nclass_windows.py\nTableAddFather\n'
            QMessageBox.critical(
                self,
                'Ошибка ввода',
                f'{answer_error()} {name}Подробности:\n {e}'
            )
        self.pushButton.setText("Закрыть окно")
        self.vl.addWidget(self.save_button)
        self.vl.addWidget(self.pushButton)
        self.table_wiew = None

    def save_data(self) -> None:
        '''Сохранение данных по отцу.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.df_res = DataFrame(
            columns=[x for x in range(self.tableView.model().columnCount())],
            index=[x for x in range(self.tableView.model().rowCount())])
        for i in range(self.tableView.model().rowCount()):
            for j in range(self.tableView.model().columnCount()):
                if self.tableView.model().index(i, j).data() != 'nan':
                    self.df_res.iloc[i, j] = self.tableView.model().index(
                        i, j
                        ).data()
        self.df_res = self.df_res.dropna(how='all')
        data_job = self.df_res
        data_job.index = self.header_labels_vertical
        data_job.columns = [0]
        data_job = data_job.T
        print(data_job)
        try:
            query = BullFather.select().where(
                BullFather.number == data_job.loc[0, 'Инвертарный номер']
            )
            if query.exists():
                QMessageBox.information(
                    self,
                    'Ответ',
                    'Такой бык уже существует!'
                )
            else:
                save_bus_data_fater(data_job)
                query = BullFather.select().where(
                    BullFather.number == data_job.loc[0, 'Инвертарный номер']
                )
                if query.exists():
                    QMessageBox.information(
                        self,
                        'Ответ',
                        'Сохранено!'
                    )

        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка ввода',
                f'{answer_error()} \nclass_window.py\n Подробности:\n {e}'
            )
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: ' +
                '0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #004524);}' +
                'QPushButton:hover {background-color: qlineargradient(x1:' +
                ' 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
            )
        )

    def validate(self, data_job: DataFrame):
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
    """
        df = pd.read_csv(
            './func/data/search_fatherh/faters.csv',
            sep=';',
            decimal=',',
            encoding='cp1251'
        )
        number_now = float(data_job.loc['Профиль', 'Инвертарный номер'])
        list_numer = list(df['Номер'].fillna(0).astype('float'))
        if number_now in list_numer:
            QMessageBox.critical(self, 'Ошибка ввода', 'Такой бык уже записан')
        return True


class TableDataEnter(QTableWidget):
    def keyPressEvent(self, event):
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            return
        super(TableDataEnter, self).keyPressEvent(event)
