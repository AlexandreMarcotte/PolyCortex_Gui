import numpy as np
# -- My packages --
from ... dock.dock import Dock
import pyqtgraph.opengl as gl
from app.pyqt_frequently_used import *
from app.activation_b import btn


class FftOverTimeGraph3D(Dock):
    def __init__(self, gv, layout):

        super().__init__(gv, 'fft', layout)
        self.gv = gv
        self.layout = layout

        self.ch = 0

        view = self.init_view()
        self.surface = self.init_surface()
        view.addItem(self.surface)
        # Add to tab layout
        self.plot_d.layout.addWidget(view, 3, 0, 1, 2)

        self.init_choose_ch_combobox()
        self.init_on_off_button()

        # self.layout.addWidget(self.secondary_gr, 0, 0)

        self.timer.timeout.connect(self.update)

    def init_view(self):
        """"""
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
        return surface

    def update(self):
        fft_over_t = np.array(self.gv.freq_calculator.fft_over_time[self.ch])
        fft_over_t /= max(fft_over_t[-1])
        self.surface.setData(z=(15*fft_over_t-7))


