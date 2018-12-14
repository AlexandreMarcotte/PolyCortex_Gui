# --General Packages--
import pyqtgraph as pg
from collections import deque
import numpy as np
# -- My packages --
from ... dock.dock import Dock
from app.pyqt_frequently_used import *


class WaveGraphOverTime(Dock):
    def __init__(self, gv, layout):
        super().__init__(gv, 'fft', layout)
        self.gv = gv
        self.layout = layout

        self.ch = 0
        self.wave_curves = []

        self.init_choose_ch_combobox()
        self.init_on_off_button()
        # freq_band_over_time

        self.plot = self.init_plot()

        self.timer.timeout.connect(self.update)

    def init_plot(self):
        """Create the plot widget and its characteristics"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Time', units='Hz')         # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        # plot.setXRange(0, 100)
        # plot.setYRange(0, 1000000)
        # Add to tab layout
        self.secondary_layout.addWidget(plot, 2, 0, 1, 2)
        for ch in range(len(self.gv.waves)):
            self.wave_curves.append(
                plot.plot(deque(np.ones(200), maxlen=200)))
            self.wave_curves[ch].setPen(pen_colors[ch])

        return plot

    def update(self):
        for i in range(len(self.gv.waves)):
            self.wave_curves[i].setData(
                    self.gv.freq_calculator.all_freq_band_over_time[
                        self.ch].wave_type_data[i])
