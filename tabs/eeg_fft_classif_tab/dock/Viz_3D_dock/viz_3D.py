from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
# -- My packages --
from app.colors import *
from app.activation_b import btn
from PyQt5 import QtGui, QtCore


class Viz3D:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        self.init_plot()

        self.traces = {}
        self.phase = 0
        self.lines = 50
        self.points = 1000
        self.y = np.linspace(-10, 10, self.lines)
        self.x = np.linspace(-10, 10, self.points)

        for i, line in enumerate(self.y):
            self.traces[i] = gl.GLLinePlotItem()
            self.w.addItem(self.traces[i])

        self.timer = QtCore.QTimer()
        self.on_off_button()

        # Create the bar chart only for the first channel
        self.timer.timeout.connect(self.update)

    def init_plot(self):
        """     """
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        # self.w.show()
        # Add to tab layout
        self.layout.addWidget(self.w, 1, 0)

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    def update(self):
        for i, line in enumerate(self.y):
            y = np.array([line] * self.points)

            amp = 10 / (i + 1)
            phase = self.phase * (i + 1) - 10
            freq = self.x * (i + 1) / 10

            sine = amp * np.sin(freq - phase)
            pts = np.vstack([self.x, y, sine]).transpose()

            self.set_plotdata(
                name=i, points=pts,
                color=pg.glColor((i, self.lines * 1.3)),
                width=1)
            self.phase -= .0002

    def on_off_button(self):
        btn('Show viz 3D', self.layout, (0, 0), func_conn=self.start,
            color=dark_blue, toggle=True)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(100)
        else:
            self.timer.stop()