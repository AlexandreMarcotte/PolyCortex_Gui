from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import numpy as np
import pyqtgraph as pg
# -- My packages --
from app.colors import *
from app.activation_b import btn


class WaveGraph:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        self.plot = self.init_plot()
        self.init_on_off_button()
        
    def init_plot(self):
        """
        """
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.setLabel(axis='left', text='Power', units='None')
        plot.plotItem.hideAxis('bottom')
        # Add graph
        x = np.arange(10)
        y = np.sin(x)
        bg1 = pg.BarGraphItem(x=x, height=y, width=1, brush='b')
        plot.addItem(bg1)

        # Add to tab layout
        self.layout.addWidget(plot, 1, 0)
        # Create the bar chart only for the first channel
        # self.timer.timeout.connect(self.update)
        mne_head = QLabel()
        mne_head.setPixmap(QtGui.QPixmap('./img/mne_head.png'))
        self.layout.addWidget(mne_head, 2, 0)
        return plot

    def init_on_off_button(self):
        btn('Show wave signal', self.layout, (0, 0), func_conn=self.start,
            color=dark_blue, toggle=True)

    def start(self):
        pass

    def update(self):
        # Remove All item from the graph
        self.plot.clear()
        y = np.random.random(10)
        bg1 = pg.BarGraphItem(x=x, height=y, width=1, brush='b')
        self.plot.addItem(bg1)
