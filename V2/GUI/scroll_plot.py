import pyqtgraph as pg


class ScrollPlot(pg.PlotWidget):
    def __init__(self, signals=()):
        super().__init__()
        self.signals = signals
        # Curve
        self.curves = self.init_curves(signals)
        # Timer
        self.timer = self.init_timer()
        self.timer.start()

    def init_timer(self):
        t = pg.QtCore.QTimer()
        t.timeout.connect(self.update)
        return t

    def init_curves(self, signals):
        curves = []
        for signal in signals:
            curves.append(self.plot(signal))
        return curves

    def update(self):
        for i, signal in enumerate(self.signals):
            self.curves[i].setData(signal)
