from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore


import numpy as np
import pyqtgraph as pg
# -- My packages --
from app.colors import *
from ... dock.dock import Dock


class WaveGraph(Dock):
    def __init__(self, gv, layout):
        super().__init__(layout)
        self.gv = gv
        self.layout = layout

        self.plot = self.init_plot()

        self.timer.timeout.connect(self.update)

    def init_plot(self):
        """
        """
        plot = super().init_plot()
        plot.plotItem.setLabel(axis='left', text='Power', units='None')
        plot.plotItem.hideAxis('bottom')
        # Add graph
        x = np.arange(10)
        y = np.sin(x)
        bg = pg.BarGraphItem(x=x, height=y, width=1, brush='b')
        plot.addItem(bg)

        # Add to tab layout
        self.layout.addWidget(plot, 1, 0)

        return plot

    def add_head_img(self):
        mne_head = QLabel()
        mne_head.setPixmap(QtGui.QPixmap('./img/mne_head.png'))
        self.layout.addWidget(mne_head, 2, 0)

    def update(self):
        # Remove All item from the graph
        self.plot.clear()
        N_ELE = 5
        y = np.random.random(N_ELE)
        x = np.array([100, ])
        bg = pg.BarGraphItem(x=x, height=y, width=[4, 4, 4, 28, 60], brush='b')
        self.plot.addItem(bg)
