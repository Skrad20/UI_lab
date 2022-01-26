import sys
import time

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QProgressIndicator(QWidget):
    m_angle = None
    m_timerId = None
    m_delay = None
    m_displayedWhenStopped = None
    m_color = None

    def __init__(self, parent, stop_thread):
        super(QProgressIndicator, self).__init__(parent)
        self.initUI('Загружаем...')
        self.vb = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('Всё работает, нужно немного подождать!')
        self.label.setWordWrap(True)
        self.vb.addWidget(self.label)
        self.setProprties()
        self.m_angle = 0
        self.m_timerId = -1
        self.m_delay = 40
        self.m_displayedWhenStopped = False
        self.m_color = Qt.black
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setFocusPolicy(Qt.NoFocus)
        self.stop_thread = stop_thread
        #self.close_progress(self.stop_thread)

    def initUI(self, name):
        """Конструктор формы"""
        self.setWindowTitle(name)
        self.setWindowIcon(QIcon('data\icon.ico'))
        self.show()

    def animationDelay(self):
        return self.delay

    def isAnimated(self):
        return (self.m_timerId != -1)

    def isDisplayedWhenStopped(self):
        return self.displayedWhenStopped

    def getColor(self):
        return self.color

    def sizeHint(self):
        return QSize(200, 150)

    def startAnimation(self):
        self.m_angle = 0

        if self.m_timerId == -1:
            self.m_timerId = self.startTimer(self.m_delay)

    def stopAnimation(self):
        if self.m_timerId != -1:
            self.killTimer(self.m_timerId)

        self.m_timerId = -1
        self.update()

    def setAnimationDelay(self, delay):
        if self.m_timerId != -1:
            self.killTimer(self.m_timerId)

        self.m_delay = delay

        if self.m_timerId != -1:
            self.m_timerId = self.startTimer(self.m_delay)

    def setDisplayedWhenStopped(self, state):
        self.displayedWhenStopped = state
        self.update()

    def setColor(self, color):
        self.m_color = color
        self.update()

    def timerEvent(self, event):
        self.m_angle = (self.m_angle + 30) % 360
        self.update()

    def paintEvent(self, event):
        if (not self.m_displayedWhenStopped) and (not self.isAnimated()):
            return
        width = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        outerRadius = (width - 1) * 0.5 * 1
        innerRadius = (width - 1) * 0.5 * 0.38

        capsuleHeight = outerRadius - innerRadius
        capsuleWidth  = capsuleHeight *.23 if (width > 32) else capsuleHeight *.35
        capsuleRadius = capsuleWidth / 2
        for i in range(0, 12):
            color = QColor(self.m_color)

        if self.isAnimated():
            color.setAlphaF(1.0 - (i / 12.0))
        else:
            color.setAlphaF(0.2)

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.save()
        painter.translate(self.rect().center())
        painter.rotate(self.m_angle - (i * 30.0))
        painter.drawRoundedRect(capsuleWidth * -0.5, (innerRadius + capsuleHeight) * -1, capsuleWidth, capsuleHeight, capsuleRadius, capsuleRadius)
        painter.restore()

    def setProprties(self):
        self.delay = pyqtProperty(int, self.animationDelay, self.setAnimationDelay)
        self.displayedWhenStopped = pyqtProperty(bool, self.isDisplayedWhenStopped, self.setDisplayedWhenStopped)
        self.color = pyqtProperty(QColor, self.getColor, self.setColor)

    def close_progress(self, stop_thread):
        if stop_thread:
            self.close()



def TestProgressIndicator(stop_thread):
    app = QApplication(sys.argv)
    progress = QProgressIndicator(None, stop_thread)
    progress.setAnimationDelay(70)
    progress.startAnimation()

    def close():
        progress.close()

    sys.exit(app.exec_())


if __name__ == "__main__":
    stop_thread = False
    TestProgressIndicator(stop_thread)
