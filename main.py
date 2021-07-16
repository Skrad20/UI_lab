#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from peewee import *
from classes.class_window import *

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r"venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = GeneralWindow()
    window.setWindowIcon(QIcon(r'data\icon.jpg'))
    window.show_window_biotech()
    print(repr(window))
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
