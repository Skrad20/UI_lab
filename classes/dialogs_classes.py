#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog, QMenu,
                             QMessageBox)

from func.func_answer_error import answer_error


class MainDialog(QDialog):
    """Окно доп вывода"""
    def __init__(self, table, name, parent=None):
        super(MainDialog, self).__init__(parent)
        self.initUI(name)
        self.tabl = table

    def botton_closed(self):
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.close()

    def initUI(self, name):
        """Конструктор формы"""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.center()
        self.setMinimumWidth(1000)
        self.setMinimumHeight(500)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.show()

    def center(self):
        """Центрирует окно"""
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().topLeft()
        qr.moveCenter(cp)
        self.move(qr.center())
        self.clipboard = []

    def eventFilter(self, source, event):
        '''Отслеживание событий вставки или копирования.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
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
            QMessageBox.critical(
                self,
                'Что-то пошло не так',
                f'{answer_error()} Подробности:\n {e}'
            )

    def copySelection(self):
        '''Копирование данных ctrl+С.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        self.clipboard.clear()
        selected = self.tableView.selectedIndexes()
        rows = []
        columns = []
        for index in selected:
            rows.append(index.row())
            columns.append(index.column())
        minRow = min(rows)
        minCol = min(columns)
        res_clipboard = []
        for index in selected:
            res_clipboard.append(
                (index.row() - minRow, index.column() - minCol, index.data())
            )
        res_str = ''
        for val in res_clipboard:
            res_str += f'\n{val[2]}'
        clipboard = QApplication.clipboard()
        clipboard.setText(res_str)

        df_in = pd.DataFrame(
            columns=[x for x in range(300)],
            index=[x for x in range(50)]
        )
        for i in range(len(res_clipboard)):
            data_copy = res_clipboard[i]
            row = data_copy[0]
            col = data_copy[1]
            data_in_df = data_copy[2]
            df_in.iloc[row, col] = data_in_df
        df_in = df_in.dropna(how='all')
        df_in = df_in.dropna(how='all', axis='columns')

    def pasteSelection(self):
        '''Вставка данных ctrl+V.'''
        """
        Описание

        Параметры:
        ----------
        
        Возвращает:
        -------
        """
        table = QApplication.clipboard()
        mime = table.mimeData()
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
