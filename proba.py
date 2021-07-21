from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QSize, Qt
import os
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
    
# Наследуемся от QMainWindow
class MainWindow(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        QMainWindow.__init__(self)
    
        self.setMinimumSize(QSize(480, 80))             # Устанавливаем размеры
        self.setWindowTitle("Работа с QTableWidget")    # Устанавливаем заголовок окна
        central_widget = QWidget(self)                  # Создаём центральный виджет
        self.setCentralWidget(central_widget)           # Устанавливаем центральный виджет
    
        grid_layout = QGridLayout()             # Создаём QGridLayout
        central_widget.setLayout(grid_layout)   # Устанавливаем данное размещение в центральный виджет
    
        table = QTableWidget(self)  # Создаём таблицу
        table.setColumnCount(3)     # Устанавливаем три колонки
        table.setRowCount(1)        # и одну строку в таблице
    
        # Устанавливаем заголовки таблицы
        table.setHorizontalHeaderLabels(["Header 1", "Header 2", "Header 3"])
    
        # Устанавливаем всплывающие подсказки на заголовки
        table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        table.horizontalHeaderItem(2).setToolTip("Column 3 ")
    
        # Устанавливаем выравнивание на заголовки
        table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)
    
        # заполняем первую строку
        table.setItem(0, 0, QTableWidgetItem("Text in column 1"))
        table.setItem(0, 1, QTableWidgetItem("Text in column 2"))
        table.setItem(0, 2, QTableWidgetItem("Text in column 3"))
    
        # делаем ресайз колонок по содержимому
        table.resizeColumnsToContents()
    
        grid_layout.addWidget(table, 0, 0)   # Добавляем таблицу в сетку
    
    
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())