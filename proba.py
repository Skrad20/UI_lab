from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.model = QtGui.QStandardItemModel(10, 10)
        self.tableView = QtWidgets.QTableView()
        self.tableView.setModel(self.model)

        self.tableView.installEventFilter(self)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.tableView)

        self.clipboard = []

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event == QtGui.QKeySequence.Copy:
                self.copySelection()
                return True
            elif event == QtGui.QKeySequence.Paste:
                self.pasteSelection()
                return True

        elif event.type() == QtCore.QEvent.ContextMenu:
            menu = QtWidgets.QMenu()
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
        return super(Window, self).eventFilter(source, event)

    def copySelection(self):
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
        print(self.clipboard[1])
        df_in = pd.DataFrame(columns=[x for x in range(300)], index=[x for x in range(50)])
        for i in range(len(self.clipboard)):
            data_copy = self.clipboard[i]
            print(data_copy)
            row = data_copy[0]
            col = data_copy[1]
            data_in_df = data_copy[2]
            df_in.iloc[row, col] = data_in_df
        df_in = df_in.dropna(how='all')
        df_in = df_in.dropna(how='all', axis='columns')


    def pasteSelection(self):
        table = QApplication.clipboard()
        mime = table.mimeData()
        data = mime.data('application/x-qt-windows-mime;value="Csv"')
        data = str(data.data())[1:]
        data = data.split(r'\r\n')
        print(data)
        columns = data[0].split(';')
        columns[0] = columns[0].replace("'", "")
        self.df = pd.DataFrame(columns=columns, index=[x for x in range(len(data))])
        for i in range(1, len(data)-1):
            data_in = data[i].split(';')
            for j in range(len(data_in)):
                self.df.iloc[i-1, j] = data_in[j]
        self.df = self.df.dropna(how='all')
        self.df = self.df.dropna(how='all', axis='columns')
        print(self.df)
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
                self.model.setData(index, data_o, QtCore.Qt.DisplayRole)
                selection.select(index, selection.Select)

        self.tableView.setSelectionModel(selection)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())