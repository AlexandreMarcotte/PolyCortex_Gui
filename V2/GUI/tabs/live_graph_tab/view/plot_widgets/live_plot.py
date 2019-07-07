from abc import abstractclassmethod
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore


class LivePlot:
    def __init__(self):
        # Timer
        self.timer = self.init_timer()
        self.timer.start(10)

    @abstractclassmethod
    def update(self):
        """Override this method to update you plot"""
        pass

    def init_timer(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        return timer

    @QtCore.pyqtSlot(bool)
    def toggle_timer(self, checked):
        if checked:
            self.timer.stop()
        else:
            self.timer.start()
