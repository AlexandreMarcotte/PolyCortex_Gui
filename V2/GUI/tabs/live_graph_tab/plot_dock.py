from pyqtgraph.dockarea import Dock
from PyQt5.QtGui import QPainter, QColor
# --My packages--
from .view.docks.fft_dock.inner_docks.plot.fft_plot import FftPlot
from V2.utils.colors import Color
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


# TODO: ALEXM: This class is ugly
class PlotDock(Dock):
    def __init__(self, plot:ScrollPlotWidget=None):
        super().__init__(name='', hideTitle=True)
        self.plot = plot
        self.other_plots = []

        self.addWidget(self.plot, 0, 1, 4, 5)

    def add_other_plot(self):
        other_plot = ScrollPlotWidget(Color.pen_colors)
        self.other_plots.append(other_plot)
        self.addWidget(other_plot, len(self.other_plots)*6, 1, 4, 5)

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
