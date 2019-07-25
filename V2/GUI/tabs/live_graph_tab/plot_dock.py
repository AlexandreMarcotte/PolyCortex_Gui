from pyqtgraph.dockarea import Dock
from PyQt5.QtGui import QPainter, QColor
# --My packages--
from .view.docks.fft_dock.inner_docks.plot.fft_plot import FftPlot


class PlotDock(Dock):
    def __init__(self, plot:FftPlot=None, other_plots=[]):
        super().__init__(name='', hideTitle=True)
        self.plot = plot
        self.other_plots = other_plots

        self.addWidget(self.plot, 0, 1, 4, 5)
        if self.other_plots:
            for p in self.other_plots:
                self.addWidget(p, 6, 1, 4, 5)

    # def add_other_plots(self):


    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self._paint_black_background(qp)
        qp.end()

    def _paint_black_background(self, qp):
        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRoundedRect(
            0, 0, self.size().width(), self.size().height(), 8, 8)
