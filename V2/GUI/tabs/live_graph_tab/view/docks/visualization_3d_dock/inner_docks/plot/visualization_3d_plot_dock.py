from pyqtgraph.dockarea import Dock
import numpy as np
# --My packages--
import pyqtgraph.opengl as gl
from .plane import Plane


class Visualization3dPlotsDock(Dock):
    def __init__(self):
        super().__init__(name='', hideTitle=True)

        self._view = self._init_plot()
        self._init_planes()
        self._view.addItem(self.plane_x)
        self._view.addItem(self.plane_y)
        self._view.addItem(self.plane_z)
        self.addWidget(self._view)

    def _init_planes(self):
        self.plane_x = Plane(
            axis='x', mvt=np.array([1, 0, 0]), key=('j', 'k'),
            rotation=(90, 0, 1, 0), color=(0, 0, 255, 4))
        self.plane_y = Plane(
            axis='y', mvt=np.array([0, 1, 0]), key=('j', 'k'),
            rotation=(90, 1, 0, 0), color=(0, 255, 0, 4))
        self.plane_z = Plane(
            axis='z', mvt=np.array([0, 0, 1]), key=('j', 'k'),
            color=(255, 0, 0, 4))

    def _init_plot(self):
        view = gl.GLViewWidget()
        view.opts['distance'] = 370
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view
