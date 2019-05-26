import pyqtgraph as pg


class BasicScrollPlot:
    def __init__(self, win, pos, display_queue):
        plot = win.addPlot(*pos)
        self.display_queue = display_queue
        self.curve = plot.plot()
        self.timer = self.init_timer()

    def init_timer(self):
        t = pg.QtCore.QTimer()
        t.timeout.connect(self.update)
        return t

    def update(self):
        self.curve.setData(self.display_queue)
