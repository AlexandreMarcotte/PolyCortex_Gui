
import numpy as np
from PyQt5 import QtCore
import pyqtgraph.opengl as gl
from pyqtgraph.dockarea import Dock
# -- My packages --
from V2.utils.create_map import create_cmap
from V2.pipeline.pipeline_stages.fft_stage.fft_stage import FftStage


class Spectrogram3dPlot(Dock):
    def __init__(self):
        super().__init__(name='', hideTitle=True)

        self.i = 0
        self.ch = 0

        view = self._init_view()
        self.addWidget(view)

        self.surface = self._init_surface()
        view.addItem(self.surface)

        self._connect_timer()

    def connect_signal(self, fft_stage: FftStage):
        self.fft_stage = fft_stage
        self.fft_over_time = self.fft_stage.fft_over_time
        self.surface.translate(0, -len(self.fft_over_time[0])//15, 0)

    def _connect_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update)

    def start_timer(self):
        self.timer.start(20)

    def _init_view(self):
        view = gl.GLViewWidget()
        view.opts['distance'] = 300
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view

    def _init_surface(self):
        surface = gl.GLSurfacePlotItem(
            shader='heightColor', computeNormals=False, smooth=False)
        surface.shader()['colorMap'] = np.array([-1, -1, -1, 0, 0, 0, 1, 1, 1])
        return surface

    def _update(self):
        self.i += 1
        fft_over_t = np.array(self.fft_over_time[self.ch])
        fft_over_t /= max(fft_over_t[-1])

        z = (15*fft_over_t-7)
        # self.x = np.linspace(0, 100, z.shape[0])
        # self.y = np.linspace(0, 100, z.shape[1])
        # self.cmap = create_cmap(z)
        # self.surface.setData(x=self.x, y=self.y, z=z, colors=self.cmap)
        self.surface.setData(z=z)


