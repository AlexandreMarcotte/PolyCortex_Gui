# --General Imports--
from scipy.signal import butter, lfilter
from copy import deepcopy
# --My Packages--
from V2.GUI.tabs.live_graph_tab.view.docks.fft_dock.filter_region import FilterRegion


class Filter:
    def __init__(self, cut_freq:[50, 70], stream_freq=250, order=5,
                 type='bandstop'):
        self.cut_freq = cut_freq
        self.stream_freq = stream_freq
        self.order = order
        self.type = type

        self.coeff = self.set_filter_coeff(cut_freq)

    def set_filter_coeff_from_filter_region(self, filter_region:FilterRegion):
        self.coeff = self.set_filter_coeff(
            (filter_region.min_boundary, filter_region.max_boundary))

    def set_filter_coeff(self, filter_bounds):
        nyq = 0.5 * self.stream_freq
        normalized_cut_freq = [coeff/nyq for coeff in filter_bounds]
        coeff = butter(
                N=self.order, Wn=normalized_cut_freq, btype=self.type,
                analog=False)
        return coeff

    def filter_signal(self, input):
        return lfilter(self.coeff[0], self.coeff[1], input)


if __name__ == '__main__':
    from pyqtgraph.Qt import QtGui
    import pyqtgraph as pg
    import numpy as np
    from numpy import pi, sin
    from collections import deque
    from time import time

    win = pg.GraphicsWindow()
    p = win.addPlot()

    N_DATA = 1250
    t = np.linspace(0, 2 * pi, N_DATA)
    data = deque(np.zeros(N_DATA), maxlen=N_DATA)
    solo_sin = deque(np.zeros(N_DATA), maxlen=N_DATA)

    itt = 0
    s2 = 1 * sin(10 * t)
    s3 = 0.4 * sin(60 * t)

    c2 = p.plot(data)
    c3 = p.plot(data)
    c3.setPen('g')

    last_t = time()
    last_n_data = 0
    once_every = 10
    filter_chunk = []

    filter = Filter(
        cut_freq=(1, 6), stream_freq=250, order=5, filter_type='bandpass')

    def update_curves():
        global data, curve, itt, last_t, last_n_data, once_every, filter_chunk, filter

        itt += 1
        data.append(s2[itt%N_DATA] + s3[itt%N_DATA])
        c2.setData(data)
        y = filter.filter_signal(data)
        c3.setData(y)
        """
        if itt % once_every == 0:
            y = filter.filter_signal(data)
            filter_chunk = list(y[-once_every:][::-1])
        # put the data once at the time at every loop so the signal is not showing
        # all jerky
        if filter_chunk != []:
            viz_data.append(filter_chunk.pop())
        c3.setData(viz_data)
        """ # version 2

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update_curves)
    timer.start(1/250 * 1000)

    QtGui.QApplication.instance().exec_()
