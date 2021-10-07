#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class Progress_diaog(QWidget):
    def __init__(self):
        super().__init__()
        self.genAudioButton = QPushButton('Generate', self)
        self.genAudioButton.clicked.connect(self.generate)
        self.show()

    def generate(self):
        try:
            info = [("hello", "1.mp4"), ("how are you?", "2.mp4"), ("StackOverFlow", "3.mp4")]
            self.progress = QProgressDialog('Work in progress', '', 0, len(info), self)
            self.progress.setWindowTitle("Generating files...")
            self.progress.setWindowModality(Qt.WindowModal)
            self.progress.show()
            self.progress.setValue(0)
        except Exception as e:
            errBox = QMessageBox()
            errBox.setWindowTitle('Error')
            errBox.setText('Error: ' + str(e))
            errBox.addButton(QMessageBox.Ok)
            errBox.exec()
            return
