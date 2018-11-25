# --General packages--
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

        self.np_zero = np.zeros(self.gv.DEQUE_LEN)

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
        self.w.opts['distance'] = 350000
        self.w.opts['center'] = QtGui.QVector3D(0, 230000, 0)
        self.w.opts['azimuth'] = 40
        self.w.opts['elevation'] = 15
        self.layout.addWidget(self.w, 1, 0)

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    def update(self):
        for ch in range(self.gv.N_CH):
            pts = np.stack((15000 * ch * np.ones(self.gv.DEQUE_LEN),
                            np.linspace(0, 400000, self.gv.DEQUE_LEN),
                            np.array(self.gv.data_queue[ch])), axis=1)

            self.set_plotdata(
                name=ch, points=pts, color=pg.glColor((ch, 8)), width=1)

    def on_off_button(self):
        btn('Show visualization 3D', self.layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(10)
        else:
            self.timer.stop()