import datetime as dt
import os

import numpy as np
import pandas as pd
from .additional_classes import TableAddFather
from .dialogs_classes import MainDialog
from .forms_classes import Form
from pandas.core.frame import DataFrame
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import (QColor, QEnterEvent, QFont, QIcon, QKeySequence,
                         QPainter, QPen, QStandardItemModel)
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDesktopWidget,
                             QGridLayout, QHBoxLayout, QLabel, QMainWindow,
                             QMenu, QMessageBox, QPushButton, QSizePolicy,
                             QSpacerItem, QTableView, QTableWidget,
                             QVBoxLayout, QWidget)

from func.func_answer_error import answer_error
from func.func_issr import issr_analit_func
from func.func_ms import (ResOut, creat_doc_pas_gen, enter_adres, ms_out_word,
                          save_file, save_file_for_word, search_father)
from func.db_job import upload_data_farmers_father
from lists_name.list_name_row import list_name_row_search_father
from models.models import Logs
from setting import DB as db
from setting import TRANSPARENCY as transparency

adres_job = ''
data_job = ''
adres_job_search_father = ''
stop_thread = False


class TitleBar(QWidget):
    # Сигнал минимизации окна
    windowMinimumed = pyqtSignal()
    # увеличить максимальный сигнал окна
    windowMaximumed = pyqtSignal()
    # сигнал восстановления окна
    windowNormaled = pyqtSignal()
    # сигнал закрытия окна
    windowClosed = pyqtSignal()
    # Окно мобильных
    windowMoved = pyqtSignal(QPoint)
    # Сигнал Своя Кнопка +++
    signalButtonMy = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TitleBar, self).__init__(*args, **kwargs)

        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.mPos = None
        self.iconSize = 20  # Размер значка по умолчанию

        # Установите цвет фона по умолчанию,
        # иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # макет
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)

        # значок окна
        self.iconLabel = QLabel(self)
#         self.iconLabel.setScaledContents(True)
        layout.addWidget(self.iconLabel)

        # название окна
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)
        layout.addWidget(self.titleLabel)

        # Средний телескопический бар
        layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Использовать шрифты Webdings для отображения значков
        font = self.font() or QFont()
        font.setFamily('Webdings')

        # Свернуть кнопку
        self.buttonMinimum = QPushButton(
            '-',
            self,
            clicked=self.windowMinimumed.emit,
            font=font,
            objectName='buttonMinimum'
        )
        layout.addWidget(self.buttonMinimum)

        # Кнопка Max / restore
        self.buttonMaximum = QPushButton(
            '+',
            self,
            clicked=self.showMaximized,
            font=font,
            objectName='buttonMaximum'
        )
        layout.addWidget(self.buttonMaximum)

        # Кнопка закрытия
        self.buttonClose = QPushButton(
            'X',
            self,
            clicked=self.windowClosed.emit,
            font=font,
            objectName='buttonClose'
        )
        layout.addWidget(self.buttonClose)

        # начальная высота
        self.setHeight()

    def showMaximized(self):
        if self.buttonMaximum.text() == '1':
            # Максимизировать
            self.buttonMaximum.setText('2')
            self.windowMaximumed.emit()
        else:  # Восстановить
            self.buttonMaximum.setText('1')
            self.windowNormaled.emit()

    def setHeight(self, height=38):
        """ Установка высоты строки заголовка """
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # Задайте размер правой кнопки  ?
        self.buttonMinimum.setMinimumSize(height, height)
        self.buttonMinimum.setMaximumSize(height, height)
        self.buttonMaximum.setMinimumSize(height, height)
        self.buttonMaximum.setMaximumSize(height, height)
        self.buttonClose.setMinimumSize(height, height)
        self.buttonClose.setMaximumSize(height, height)

    def setTitle(self, title):
        """ Установить заголовок """
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """ настройки значокa """
        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size):
        """ Установить размер значка """
        self.iconSize = size

    def enterEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super(TitleBar, self).enterEvent(event)

    def mouseDoubleClickEvent(self, event):
        super(TitleBar, self).mouseDoubleClickEvent(event)
        self.showMaximized()

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()


# Перечислить верхнюю левую, нижнюю правую и четыре неподвижные точки
Left, Top, Right, Bottom, LeftTop, RightTop, LeftBottom, RightBottom = range(8)


class Window_main(QWidget):
    """Рабочее окно программы."""
    def __init__(self, name: str, *args, **kwargs):
        super(Window_main, self).__init__(*args, **kwargs)
        self.Margins = 5
        self._pressed = False
        self.Direction = None

        # Фон прозрачный
        if transparency:
            self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Нет границы
        self.setWindowFlag(Qt.FramelessWindowHint)
        # Отслеживание мыши
        self.setMouseTracking(True)
        # макет
        self.vb = QVBoxLayout(self, spacing=0)
        # Зарезервировать границы для изменения размера окна без полей
        self.vb .setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)
        # Панель заголовка
        self.titleBar = TitleBar(self)
        self.vb.addWidget(self.titleBar)

        # слот сигнала
        self.titleBar.windowMinimumed.connect(self.showMinimized)
        self.titleBar.windowMaximumed.connect(self.showMaximized)
        self.titleBar.windowNormaled.connect(self.showNormal)
        self.titleBar.windowClosed.connect(self.close)
        self.titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)
        self.name = name
        self.initUI(name)
        self.adres_res = ''
        self.db = db
        log_1 = Logs(name='Запуск основного окна')
        log_1.save()
        self.setWindowFlags(Qt.FramelessWindowHint)

    def setTitleBarHeight(self, height=38):
        """ Установка высоты строки заголовка """
        self.titleBar.setHeight(height)

    def setIconSize(self, size):
        """ Установка размера значка """
        self.titleBar.setIconSize(size)

    def setWidget(self, widget):
        """ Настройте свои собственные элементы управления """
        if hasattr(self, '_widget'):
            return
        self._widget = widget
        # Установите цвет фона по умолчанию,
        # иначе он будет прозрачным из-за влияния родительского окна
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, QColor(240, 240, 240))
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def move(self, pos):
        if (
            self.windowState() == Qt.WindowMaximized or
            self.windowState() == Qt.WindowFullScreen
        ):
            # Максимизировать или полноэкранный режим не допускается
            return
        super(Window_main, self).move(pos)

    def showMaximized(self):
        """ Чтобы максимизировать, удалите верхнюю, нижнюю, левую и правую границы.
            Если вы не удалите его, в пограничной области будут пробелы. """
        super(Window_main, self).showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """ Восстановить, сохранить верхнюю и нижнюю левую и правую границы,
            иначе нет границы, которую нельзя отрегулировать """
        super(Window_main, self).showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        """ Фильтр событий, используемый для решения мыши в других элементах
            управления и восстановления стандартного стиля мыши """
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)
        return super(Window_main, self).eventFilter(obj, event)

    def paintEvent(self, event):
        """
        Поскольку это полностью прозрачное фоновое окно, жесткая для поиска
        граница с прозрачностью 1 рисуется в событии перерисовывания,
        чтобы отрегулировать размер окна.
        """
        super(Window_main, self).paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        """ Событие клика мыши """
        super(Window_main, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self._mpos = event.pos()
            self._pressed = True

    def mouseReleaseEvent(self, event):
        ''' Событие отказов мыши '''
        super(Window_main, self).mouseReleaseEvent(event)
        self._pressed = False
        self.Direction = None

    def mouseMoveEvent(self, event):
        """ Событие перемещения мыши """
        super(Window_main, self).mouseMoveEvent(event)
        pos = event.pos()
        xPos, yPos = pos.x(), pos.y()
        wm, hm = self.width() - self.Margins, self.height() - self.Margins
        if self.isMaximized() or self.isFullScreen():
            self.Direction = None
            self.setCursor(Qt.ArrowCursor)
            return
        if event.buttons() == Qt.LeftButton and self._pressed:
            self._resizeWidget(pos)
            return
        if xPos <= self.Margins and yPos <= self.Margins:
            # Верхний левый угол
            self.Direction = LeftTop
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos <= self.width() and hm <= yPos <= self.height():
            # Нижний правый угол
            self.Direction = RightBottom
            self.setCursor(Qt.SizeFDiagCursor)
        elif wm <= xPos and yPos <= self.Margins:
            # верхний правый угол
            self.Direction = RightTop
            self.setCursor(Qt.SizeBDiagCursor)
        elif xPos <= self.Margins and hm <= yPos:
            # Нижний левый угол
            self.Direction = LeftBottom
            self.setCursor(Qt.SizeBDiagCursor)
        elif 0 <= xPos <= self.Margins and self.Margins <= yPos <= hm:
            # Влево
            self.Direction = Left
            self.setCursor(Qt.SizeHorCursor)
        elif wm <= xPos <= self.width() and self.Margins <= yPos <= hm:
            # Право
            self.Direction = Right
            self.setCursor(Qt.SizeHorCursor)
        elif self.Margins <= xPos <= wm and 0 <= yPos <= self.Margins:
            # выше
            self.Direction = Top
            self.setCursor(Qt.SizeVerCursor)
        elif self.Margins <= xPos <= wm and hm <= yPos <= self.height():
            # ниже
            self.Direction = Bottom
            self.setCursor(Qt.SizeVerCursor)

    def _resizeWidget(self, pos):
        """ Отрегулируйте размер окна """
        if self.Direction is None:
            return
        mpos = pos - self._mpos
        xPos, yPos = mpos.x(), mpos.y()
        geometry = self.geometry()
        x, y, w, h = (
            geometry.x(), geometry.y(),
            geometry.width(), geometry.height()
        )
        if self.Direction == LeftTop:          # Верхний левый угол
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
        elif self.Direction == RightBottom:    # Нижний правый угол
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
        elif self.Direction == RightTop:       # верхний правый угол
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos.setX(pos.x())
        elif self.Direction == LeftBottom:     # Нижний левый угол
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos.setY(pos.y())
        elif self.Direction == Left:            # Влево
            if w - xPos > self.minimumWidth():
                x += xPos
                w -= xPos
            else:
                return
        elif self.Direction == Right:           # Право
            if w + xPos > self.minimumWidth():
                w += xPos
                self._mpos = pos
            else:
                return
        elif self.Direction == Top:             # выше
            if h - yPos > self.minimumHeight():
                y += yPos
                h -= yPos
            else:
                return
        elif self.Direction == Bottom:          # ниже
            if h + yPos > self.minimumHeight():
                h += yPos
                self._mpos = pos
            else:
                return
        self.setGeometry(x, y, w, h)

    def initUI(self, name):
        """Конструктор формы"""
        self.center()
        self.setMinimumWidth(400)
        self.setMinimumHeight(550)
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.show()

    def center(self):
        """Центрирует окно"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def button_creat(
            self,
            func,
            label: str,
            text: str = None,
            class_func=None
    ) -> None:
        """Создает кнопку в окне программы."""
        self.button = QPushButton()
        self.button.setText(label)
        self.button.clicked.connect(func)
        if text is not None:
            self.button.setToolTip(F"<h3>{text}</h3>")
        self.vb.addWidget(self.button)

    def button_creat_double(
            self,
            func_first,
            label_first: str,
            func_second,
            label_second: str,
            class_func=None
    ) -> None:
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


class WindowAddFatter(Window_main):
    '''Рабочее окно для добавления отцов.'''
    def __init__(self, name: str):
        super().__init__(name=None)
        log_2 = Logs(name='Добавление отца')
        log_2.save()

        text_1 = 'Внести отцов в базу'
        labe_text = QLabel(text_1)
        labe_text.setAlignment(Qt.AlignCenter)
        self.vb.addWidget(labe_text)

    def data_result_in(self):
        self.window = TableAddFather(
            None,
            'Biotech Lab: enter data',
            None,
            self
        )
        self.window.show()
        self.window.exec_()


class Wind_Table_GP_invertory(MainDialog):
    '''Окно для ввода описи.'''
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.model = QStandardItemModel(500, 7)
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
            columns=[x for x in range(self.tableView.model().columnCount())],
            index=[x for x in range(self.tableView.model().rowCount())])
        for i in range(self.tableView.model().rowCount()):
            for j in range(self.tableView.model().columnCount()):
                if self.tableView.model().index(i, j).data() != 'nan':
                    self.df_res.iloc[i, j] = (self.tableView.model().index(
                        i, j
                        ).data())
        self.df_res = self.df_res.dropna(how='all')
        data_job = self.df_res
        data_job.columns = self.header_labels
        data_job.to_csv(
            r'func\data\creat_pass_doc\inventory_aus_table.csv',
            sep=';',
            decimal=',',
            encoding='cp1251',
            index=False
        )
        self.adres_job_res = (
            r'func\data\creat_pass_doc\i' +
            r'nventory_aus_table.csv'
        )
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: 0, ' +
                'y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b);}' +
                'QPushButton:hover {background-color: qlineargradient(' +
                'x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: ' +
                '1 #132712);}'
            )
        )


class Wind_Table_GP_profils(MainDialog):
    '''Окно для ввода описи.'''
    def __init__(self, table, name, parent):
        super().__init__(table, name, parent=parent)
        self.model = QStandardItemModel(500, 31)
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
        data_job.columns = self.header_labels
        data_job.to_csv(
            r'func\data\creat_pass_doc\profils_aus_table.csv',
            sep=';',
            decimal=',',
            encoding='cp1251',
            index=False
        )
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: 0,' +
                ' y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #004524);}' +
                'QPushButton:hover {background-color: qlineargradient(x1: 0,' +
                ' y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 #132712);}'
            )
        )


class WindowISSR(Window_main):
    '''Рабочее окно для обработки ISSR.'''
    def __init__(self, name: str):
        super().__init__(name)
        log = Logs(name='Сбор паспортов ISSR')
        log.save()
        text_1 = 'Здесь можно обработать первичные данные по ISSR'
        self.label_creat(text_1)

        self.button_layout = QHBoxLayout()
        self.button_1 = QPushButton()
        self.button_1.setText('Результаты ISSR')
        self.button_1.setToolTip(
            "<h3>Выберите файл с результатми ISSR</h3>"
        )
        self.button_1.clicked.connect(self.gen_issr)

        self.button_2 = QPushButton()
        self.button_2.setText('Пример')
        self.button_2.setToolTip(
            "<h3>Посмотрите пример оформления результатов</h3>"
        )
        self.button_2.clicked.connect(self.example_issr)

        self.button_1.setMinimumHeight(100)
        self.button_2.setMinimumHeight(100)

        self.button_layout.addWidget(self.button_1)
        self.button_layout.addWidget(self.button_2)
        self.vb.addLayout(self.button_layout)

        self.button_layout_2 = QHBoxLayout()
        self.button_3 = QPushButton()
        self.button_3.setText('Обработать')
        self.button_3.clicked.connect(self.analis_issr)
        self.vb.addWidget(self.button_3)

    def gen_issr(self) -> None:
        '''Ввод результатов ISSR'''
        self.adres_issr_in = enter_adres('Добавить данные по ISSR')
        if self.adres_issr_in != '':
            self.button_1.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(x1: ' +
                    '0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, ' +
                    'stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: qlineargradient(' +
                    'x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 ' +
                    ' #132712);}'
                )
            )

    def example_issr(self) -> None:
        '''Вывод примера оформления'''
        df_example_inventiry = pd.read_csv(
            r'func\data\issr\issr.txt',
            sep='\t',
            decimal=',',
            encoding='cp1251'
        )
        table_wiew = ResOut(df_example_inventiry)
        dialog = WindowTabl(table_wiew, 'Biotech Lab: example ISSR', self)
        dialog.exec_()

    def analis_issr(self) -> None:
        '''Анализ issr'''
        try:
            self.res_df_issr = issr_analit_func(self.adres_issr_in)
            self.adres_res = save_file(self.res_df_issr)
            global adres_job
            adres_job = self.adres_res
            self.button_creat(
                self.open_file_result,
                'Открыть файл с результатами'
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                'Ошибка ввода',
                f'{answer_error()} Подробности:\n {e}'
            )


class WindowGenPassWord(Window_main):
    '''Рабочее окно для данных из word.'''
    def __init__(self, name: str):
        super().__init__(name)
        log_3 = Logs(name='Сбор паспортов')
        log_3.save()
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
            self.button_1.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(' +
                    'x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: ' +
                    '1 #00140b);}' +
                    'QPushButton:hover {background-color: ' +
                    'qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, ' +
                    'stop: 0 #468f42, stop: 1 #132712);}'
                )
            )

    def add_data_in_table_invertory(self) -> None:
        '''Выводит окно для вставки данных описей в таблицу.'''
        self.adres_invertory = (
            r"func\data\creat_pass_doc" +
            r'\inventory_aus_table.csv'
        )
        try:
            self.window = Wind_Table_GP_invertory(
                None,
                'Biotech Lab: enter data invertory',
                self
            )
            self.window.show()
            self.window.exec_()
            self.button_5.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(x1: 0,' +
                    ' y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #00140b' +
                    ');}' +
                    'QPushButton:hover {background-color: qlineargradient' +
                    '(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: 1 ' +
                    '#132712);}'
                )
            )
        except Exception as e:
            name = 'add_data_in_table_invertory'
            QMessageBox.critical(
                self,
                'Что-то пошло не так',
                f'{answer_error()} \n{name}\n Подробности:\n {e}'
            )

    def add_data_in_table_profils(self) -> None:
        '''Выводит окно для вставки данных профилей в таблиц.'''
        try:
            self.adres_genotyping = (
                r'func\data\creat_pass_doc' +
                r'\profils_aus_table.csv'
            )
            self.window = Wind_Table_GP_profils(
                None,
                'Biotech Lab: enter data invertory',
                self
                )
            self.window.show()
            self.window.exec_()
            self.button_6.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient(x1: 0, ' +
                    ' y1: 0, x2: 1, y2: 1, stop: 0 #00e074, ' +
                    'stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: qlineargradient(' +
                    'x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, ' +
                    'stop: 1 #132712);}'
                )
            )
        except Exception as e:
            name = 'add_data_in_table_profils'
            QMessageBox.critical(
                self,
                'Что-то пошло не так',
                f'{answer_error()} \n{name}\nПодробности:\n {e}'
            )

    def gen_password_genotyping(self) -> None:
        """Генерирует запись о добавленых данных"""
        self.adres_genotyping = enter_adres(
            'Добавить данные по генотипированию'
        )
        if self.adres_genotyping != '':
            self.button_3.setStyleSheet(
                (
                    'QPushButton {background-color: qlineargradient' +
                    '(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, ' +
                    'stop: 1 #00140b);}' +
                    'QPushButton:hover {background-color: ' +
                    'qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, ' +
                    'stop: 0 #468f42, stop: 1 #132712);}'
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
        df_example_inventiry = pd.read_csv(
            r'func\data\creat_pass_doc\inventory_example.csv',
            sep=';',
            decimal=',',
            encoding='cp1251'
        )
        table_wiew = ResOut(df_example_inventiry)
        dialog = WindowTabl(
            table_wiew,
            'Biotech Lab: example inventiry',
            self
        )
        dialog.exec_()

    def example_genotyping(self) -> None:
        '''Открывает файл пример для генотипирования.'''
        df_example_genotyping = pd.read_csv(
            r'func\data\creat_pass_doc\profils_example.csv',
            sep=';',
            decimal=',',
            encoding='cp1251')
        table_wiew = ResOut(df_example_genotyping)
        dialog = WindowTabl(
            table_wiew,
            'Biotech Lab: example genotyping',
            self
        )
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
            QMessageBox.critical(
                self,
                'Ошибка ввода',
                f'{answer_error()} Подробности:\n {e}'
            )


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
        self.setWindowIcon(QIcon('data/icon.ico'))
        self.show()


class WindowSearchFarher(Window_main):
    '''Рабочее окно для поиска возможных отцов.'''
    def __init__(self, name: str):
        super().__init__(name)
        log_2 = Logs(name='Поиск отцов')
        log_2.save()
        self.hosbut_all = {
            'Выбрать всех': False
        }
        text_2 = 'Выберите хозяйства'
        labe_text_2 = QLabel(text_2)
        labe_text_2.setAlignment(Qt.AlignCenter)
        self.vb.addWidget(labe_text_2)
        farmers = upload_data_farmers_father()
        print(farmers)
        list_farmers = list(farmers)
        list_farmers_in = []
        for i in range(len((list_farmers))):
            try:
                split_farm = list_farmers[i].split(', ')
                for name in split_farm:
                    name = name.replace(' ', '')
                    list_farmers_in.append(name)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Ошибка ввода',
                    f'{answer_error()} Подробности:\n {e}'
                )

        farmers_end = []
        for farme in list_farmers_in:
            if farme is np.nan:
                pass
            elif farme == 'nan':
                pass
            else:
                farmers_end.append(farme)

        farmers_end.append('Выбрать всех')
        farmers_end = list(set(farmers_end))
        hosbut = farmers_end.copy()
        hosbut_chek = {
        }
        for name in hosbut:
            hosbut_chek[name] = QCheckBox(name, self)
            hosbut_chek[name].stateChanged.connect(
                lambda checked,
                res=name: self.check_answer(checked, res)
            )
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

    def res_search_cow_father(self, class_func=None) -> None:
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
            QMessageBox.critical(
                self,
                'Ошибка ввода',
                f'{answer_error()} Подробности:\n {e}'
            )

    def data_result_in(self):
        self.window = WindowTableEnterDataSF(
            None,
            'Biotech Lab: enter data',
            self.hosbut_all, self)
        self.window.show()
        self.window.exec_()


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
            name = 'WindowMSAusWord res_ms_aus_word_in_csv'
            QMessageBox.information(
                self,
                'Ошибка ввода',
                f'{answer_error()} \n{name}\nПодробности:\n {e}'
            )


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
        self.installEventFilter(self)
        print(self.tabl)
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

    def eventFilter(self, source, event):
        '''Отслеживание событий вставки или копирования.'''
        try:
            if event.type() == QEvent.KeyPress:
                if event == QKeySequence.Copy:
                    print('copy')
                    self.copySelection()
                    return True
            elif event.type() == QEvent.ContextMenu:
                menu = QMenu()
                copyAction = menu.addAction('Copy')
                copyAction.triggered.connect(self.copySelection)
                if not self.tabl.selectedIndexes():
                    copyAction.setEnabled(False)
                menu.exec(event.globalPos())
                return True
            return False
        except Exception as e:
            name = "WindowResulWiew eventFilter"
            QMessageBox.critical(
                self,
                'Что-то пошло не так',
                f'{answer_error()} \n{name}\nПодробности:\n {e}'
            )
        return False

    def copySelection(self):
        '''Копирование данных ctrl+С.'''
        self.clipboard.clear()
        selected = self.tabl.selectedIndexes()
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


class WindowTableEnterDataSF(MainDialog):
    """Окно для для ввода данных по потомку."""
    def __init__(self, table, name, hosbut_all, parent):
        super().__init__(table, name, parent=parent)
        self.hosbut_all = hosbut_all
        self.model = QStandardItemModel(19, 1)
        self.tableView = QTableView()
        header_labels = ['Потомок']
        self.model.setHorizontalHeaderLabels(header_labels)
        self.header_labels_vertical = list_name_row_search_father
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
        data_job.columns = ['Потомок']
        data_job['Локус'] = self.header_labels_vertical
        data_job = data_job[['Локус', 'Потомок']]
        data_job.to_csv(
            r'func\data\search_fatherh\bus_search_in_table.csv',
            sep=';',
            decimal=',',
            encoding='cp1251',
            index=False
        )
        global adres_job_search_father
        adres_job_search_father = (
            r'func\data\search_fatherh' +
            r'\bus_search_in_table.csv'
        )
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
            name = 'save_data WindowTableEnterDataSF'
            QMessageBox.critical(
                self,
                'Ошибка ввода',
                f'{answer_error()} \n{name}\nПодробности:\n {e}')
        self.save_button.setStyleSheet(
            (
                'QPushButton {background-color: qlineargradient(x1: ' +
                '0, y1: 0, x2: 1, y2: 1, stop: 0 #00e074, stop: 1 #004524);}' +
                'QPushButton:hover {background-color: qlineargradient(' +
                'x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #468f42, stop: ' +
                '1 #132712);}'
            )
        )


class SecondWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./classes/t.ui', self)


class WindowTest(Window_main):
    """Окно для тестирования функций."""
    def __init__(self, name: str):
        super().__init__(name)
        print('dfgdfgdf')
