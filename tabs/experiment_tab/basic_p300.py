from pyqtgraph.dockarea import *
import pyqtgraph as pg
import numpy as np

class BasicP300:
    def __init__(self, area, below_dock):
        self.name = 'Basic P300'

        self.instantiate_plot()

        self.init_dock(area, below_dock)

    def init_dock(self, area, below_dock):
        dock = Dock(self.name)
        area.addDock(dock, 'above', below_dock)

        layout = pg.LayoutWidget()
        dock.addWidget(layout)

        plot = self.instantiate_plot()
        layout.addWidget(plot, 0, 0)

    def instantiate_plot(self):
        plot = pg.PlotWidget()
        plot.setYRange(0, 10)
        plot.setXRange(0, 10)
        plot.plotItem.hideAxis('bottom')
        plot.plotItem.hideAxis('left')

        for i in np.linspace(1, 9, 40):
            h_line = pg.InfiniteLine(angle=0, pos=i, movable=False, pen='r')
            # v_line = pg.InfiniteLine(angle=90, pos=1, movable=False)
            # self.emg_plot.addItem(vLine, ignoreBounds=True)
            plot.addItem(h_line, ignoreBounds=True)
        # plot.addItem(v_line, ignoreBounds=True)
        return plot