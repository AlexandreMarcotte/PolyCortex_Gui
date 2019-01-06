# --General Packages--
from PyQt5 import QtCore
import pyqtgraph as pg
# --My Packages--
# Classification
from app.colors import *
from app.activation_b import btn
from .classification_graph import ClassifGraph


class ClassifPlotCreator:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout
        self.timer = QtCore.QTimer()

        self.init_show_classif_plot()

    def init_show_classif_plot(self):
        bar_chart = self.create_bar_chart()
        n_classif_plot = self.create_n_classif_plot()
        self.on_off_button()
        # Create the object to update the bar chart graph and the line graph
        self.classification_graph = ClassifGraph(
                self.gv, bar_chart, n_classif_plot)
        self.timer.timeout.connect(self.classification_graph.update_all)

    def create_bar_chart(self):
        # --- Bar chart ---
        bar_chart = pg.PlotWidget(background=dark_grey)
        bar_chart.plotItem.setLabel(axis='left', text='Power', units='None')
        bar_chart.setYRange(0, 6)
        # Add to tab layout
        self.layout.addWidget(bar_chart, 1, 0)
        return bar_chart

    def create_n_classif_plot(self):
        """Number of classification per type graph
           create the plot widget and its characteristics """
        n_classif_plot = pg.PlotWidget(background=dark_grey)
        n_classif_plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        n_classif_plot.plotItem.setLabel(axis='bottom',
                                         text='n classification time')
        n_classif_plot.plotItem.setLabel(axis='left', text='n classification')
        # Add to tab layout
        self.layout.addWidget(n_classif_plot, 2, 0)
        return n_classif_plot

    def on_off_button(self):
        """Assign pushbutton for starting and stoping the stream"""
        btn('Start classification', self.layout, (0, 0),
            func_conn=self.start, color=dark_blue_tab, toggle=True,
            txt_color=white)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(100)
        else:
            self.timer.stop()