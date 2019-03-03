# --General Packages--
import numpy as np
# --My packages--
from ... dock.dock import Dock
import pyqtgraph.opengl as gl
import matplotlib.pyplot as plt
from app.pyqt_frequently_used import create_cmap


class Spectogram3D(Dock):
    def __init__(self, gv, layout):

        super().__init__(gv, 'fft', layout)
        self.i = 0

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
        # surface = gl.GLSurfacePlotItem()
        surface = gl.GLSurfacePlotItem(
                shader='heightColor', computeNormals=False, smooth=False)
        surface.translate(0, -self.gv.DEQUE_LEN/15, 0)
        surface.shader()['colorMap'] = np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
        return surface


    def update(self):
        self.i += 1
        fft_over_t = np.array(self.gv.freq_calculator.fft_over_time[self.ch])
        fft_over_t /= max(fft_over_t[-1])

        z = (15*fft_over_t-7)
        # self.x = np.linspace(0, 100, z.shape[0])
        # self.y = np.linspace(0, 100, z.shape[1])
        # self.cmap = create_cmap(z)
        # self.surface.setData(x=self.x, y=self.y, z=z, colors=self.cmap)

        self.surface.setData(z=z)



