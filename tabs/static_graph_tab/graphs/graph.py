import os
from app.colors import *
import pyqtgraph as pg


class Graph:
    def __init__(self):
        self.plot = pg.PlotWidget()
        # self.curve = None

    def add_plot(self, layout, y=0, x=0, h=1, w=1, x_range=10000,
                 hide_axis=False, show_grid=False, alpha=0.5):
        if x_range:
            self.plot.setXRange(0, x_range)
        if hide_axis:
            self.plot.plotItem.hideAxis('bottom')
        if show_grid:
            self.plot.plotItem.showGrid(y=True, alpha=alpha)

        layout.addWidget(self.plot, y, x, h, w)

    def plot_data(self, data, color):
        curve = self.plot.plot(data, pen=color)
        self.plot.setAutoVisible(y=True)
        return curve
        
    def add_region(self, bounds, brush_color=blue, movable=True):
        """ Add a pyqtgraph region on a single event """
        self.region = pg.LinearRegionItem(movable=movable)
        self.region.setRegion(bounds)
        self.region.start_pos = bounds[0]
        self.region.last_pos = bounds[0]
        self.plot.addItem(self.region, ignoreBounds=True)
        self.region.setBrush(brush_color)