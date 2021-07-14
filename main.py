#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from peewee import *
from classes.class_window import *


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = GeneralWindow()
    window.show_window_biotech()
    print(repr(window))
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
