# --General Packages--
import pyqtgraph as pg
from collections import deque
import numpy as np
# -- My packages --
from ... dock.dock import Dock
from app.pyqt_frequently_used import *


class PowerBandGraphOverTime(Dock):
    def __init__(self, gv, layout):
        super().__init__(gv, 'fft', layout)
        self.gv = gv
        self.layout = layout

        self.pos = 0
        self.ch = 0
        self.wave_curves = []

        self.init_choose_ch_combobox()
        self.init_on_off_button()
        # freq_band_over_time

        self.plot = self.init_plot()
        self.curves_points = self.add_curvepoint_legend()

        self.timer.timeout.connect(self.update)

    def init_plot(self):
        """Create the plot widget and its characteristics"""
        plot = pg.PlotWidget(background=dark_grey)
        plot.plotItem.showGrid(x=True, y=True, alpha=0.3)
        plot.plotItem.setLabel(axis='bottom', text='Time', units='Hz')         # TODO: ALEXM : verifier l'uniter
        plot.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        plot.setXRange(0, 200)
        # plot.setYRange(0, 1000000)
        # Add to tab layout
        self.plot_d.layout.addWidget(plot, 2, 0, 1, 2)
        for ch in range(len(self.gv.waves)):
            self.wave_curves.append(
                plot.plot(deque(np.ones(200), maxlen=200)))
            self.wave_curves[ch].setPen(pen_colors[ch])

        return plot

    # TODO: ALEXM: Create an object from that
    def add_curvepoint_legend(self):
        curve_points = []
        for ch, (wave_curve, wave_name) \
                in enumerate(zip(self.wave_curves, self.gv.waves)):
            curve_points.append(pg.CurvePoint(wave_curve))
            self.plot.addItem(curve_points[ch])
            text = pg.TextItem(wave_name, anchor=(0.5, -1.0))
            text.setParentItem(curve_points[ch])
            arrow = pg.ArrowItem(angle=90)
            arrow.setParentItem(curve_points[ch])
        return curve_points

    def update(self):
        for ch in range(len(self.gv.waves)):
            new_data = self.gv.freq_calculator.all_freq_band_over_time[
                            self.ch].wave_type_data[ch]
            self.update_curves(ch, new_data)
            self.update_curve_points(ch)

    def update_curve_points(self, ch):
        self.pos += 1
        self.curves_points[ch].setPos(self.pos)

    def update_curves(self, ch, new_data):
        self.wave_curves[ch].setData(new_data)


