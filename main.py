#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtWidgets import QApplication, QMessageBox

from classes.general_window import GeneralWindow
from func.func_answer_error import answer_error
from style.style_windows import style_upload

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = (
    r"venv\Lib\site-packages\PyQt5" +
    r"\Qt5\plugins\platforms"
)

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
        QMessageBox.critical(
            None,
            'Что-то пошло не так',
            f'{answer_error()} Подробности:\n {e}'
        )
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
