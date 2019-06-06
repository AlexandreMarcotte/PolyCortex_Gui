from abc import abstractclassmethod
import pyqtgraph as pg


class LivePlot:
    @abstractclassmethod
    def update(self):
        """Override this method to update you plot"""
        pass

    def init_timer(self):
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(self.update)
        return timer
