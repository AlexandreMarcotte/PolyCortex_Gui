from PyQt5.QtWidgets import *

import numpy as np
import pyqtgraph as pg


class WaveGraph:
    def __init__(self, gv, main_window, layout):
        self.gv = gv
        self.main_window = main_window
        self.layout = layout

        # self.q = self.gv.data_queue[0]

        self.plot = self.init_plot()
        self.init_on_off_button()
        
    def init_plot(self):
        """
        """
        plot = pg.PlotWidget(background=(3, 3, 3))
        plot.plotItem.setLabel(axis='left', text='Power', units='None')
        plot.plotItem.hideAxis('bottom')
        # Add graph
        x = np.arange(10)
        y = np.sin(x)
        bg1 = pg.BarGraphItem(x=x, height=y, width=1, brush='b')
        plot.addItem(bg1)

        # Add to tab layout
        self.layout.addWidget(plot, 1, 0, 1, 1)
        # Create the bar chart only for the first channel
        return plot
        # self.timer.timeout.connect(self.update)
        """
        mne_head = QLabel(self.main_window)
        mne_head.setPixmap(QtGui.QPixmap('./logo/mne_head.png'))
        row=2; col=0; rowspan=1; colspan=1
        self.wave_layout.addWidget(mne_head, row, col, rowspan, colspan)
        """

    def init_on_off_button(self):
        b = QPushButton('Show wave signal', self.main_window)
        b.setStyleSheet("background-color: rgba(0, 0, 80, 0.4)")
        self.layout.addWidget(b, 0, 0, 1, 1)

    def update(self):
        # Remove All item from the graph
        self.plot.clear()
        y = np.random.random(10)
        bg1 = pg.BarGraphItem(x=x, height=y, width=1, brush='b')
        self.plot.addItem(bg1)
