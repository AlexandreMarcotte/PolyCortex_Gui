from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from timeit import timeit, Timer
import numpy as np
import pyqtgraph as pg
# -- My packages --
from app.colors import *
from ... dock.dock import Dock
import pyqtgraph.opengl as gl
from app.pyqt_frequently_used import *


class FftOverTimeGraph(Dock):
    def __init__(self, gv, layout):
        super().__init__(gv, layout, 'fft', 'Start')
        self.gv = gv
        self.layout = layout

        plot_gr, self.plot_layout = create_gr()
        self.layout.addWidget(plot_gr, 0, 0)
        self.init_on_off_button()

        self.view = self.init_view()
        self.plot = self.init_surface()
        self.init_choose_ch_combobox()
        self.timer.timeout.connect(self.update)

    def init_view(self):
        """     """
        view = gl.GLViewWidget()
        view.opts['distance'] = 300
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view

    def init_surface(self):
        """"""
        surface = gl.GLSurfacePlotItem(
                shader='heightColor', computeNormals=False, smooth=False)
        surface.translate(0, -self.gv.DEQUE_LEN/15, 0)
        surface.shader()['colorMap'] = np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
        self.view.addItem(surface)
        # Add to tab layout
        self.layout.addWidget(self.view, 1, 0)
        return surface

    def update(self):
        fft_over_t = np.array(self.gv.freq_calculator.fft_over_time[0])
        fft_over_t /= max(fft_over_t[-1])
        self.plot.setData(z=(15*fft_over_t-7))

    def init_choose_ch_combobox(self):
        create_param_combobox(
            self.plot_layout, 'Channels', (0, 1),
            [str(ch) for ch in range(self.gv.N_CH)],
            self.print_ch)

    def print_ch(self, ch):
        print('ch: ', ch)
