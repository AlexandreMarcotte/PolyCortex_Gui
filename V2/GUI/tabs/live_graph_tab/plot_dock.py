# --My packages--
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget
from pyqtgraph.dockarea import Dock
from PyQt5.QtGui import QPainter, QColor


class PlotDock(Dock):
    def __init__(self, plot=ScrollPlotWidget):
        super().__init__(name='', hideTitle=True)
        self.plot = plot

        self.addWidget(self.plot, 0, 1, 4, 5)

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
#
#
