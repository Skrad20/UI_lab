#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from peewee import *
from classes.class_window import *
from style.style_windows import *
from func.func_answer_error import answer_error
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'mycompany.myproduct.subproduct.version'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


def main():
    try:
        
        app = QApplication(sys.argv)
        app.setStyle("Breeze")
        app.setStyleSheet(style_upload())
        window = GeneralWindow()
        window.show_window_biotech()
        print(repr(window))
    except Exception as e:
        QMessageBox.critical(self, 'Что-то пошло не так', f'{answer_error()} Подробности:\n {e}')
    sys.exit(app.exec_())
    print('Вот и всё!')


if __name__ == "__main__":
    main()
