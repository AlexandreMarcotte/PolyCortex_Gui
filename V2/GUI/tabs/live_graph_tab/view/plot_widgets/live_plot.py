from abc import abstractclassmethod
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore


class LivePlot:
    def __init__(self):
        self.timer = None

    @abstractclassmethod
    def _update(self):
        """Override this method to update you plot"""
        pass

    def init_timer(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self._update)
        return timer

    @QtCore.pyqtSlot(bool)
    def toggle_timer(self, checked):
        if checked:
            self.timer.stop()
        else:
            self.timer.start()

    def start_aliasing(self, txt):  # Need to do it before creating the graph
        # (don't work here but work when called in the main at the start)
        # Make it look WAY better but it is a bit more laggy, set it as a setting that can be activated
        if txt == 'on':
            pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
        elif txt == 'off':
            pg.setConfigOptions(antialias=False)
