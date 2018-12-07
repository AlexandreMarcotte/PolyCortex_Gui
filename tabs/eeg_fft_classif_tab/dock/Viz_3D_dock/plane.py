# --General Packages--
import pyqtgraph.opengl as gl
import numpy as np
from .moving_object import MovingObject


class Plane(MovingObject):
    def __init__(self, rotation=(0, 1, 0, 0), scale=1, color=(0.4, 0, 0, 0.5),
                 update_func='move plane', listening_process=False):
        super().__init__(self, update_func, listening_process)
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.item = self.init_plane_item()

    def init_plane_item(self):
        item = gl.GLSurfacePlotItem(computeNormals=False, smooth=False,
                                     shader='balloon', color=self.color)
        item.scale(self.scale, self.scale, 1)
        item.translate(-50, -50, 0)
        item.rotate(*self.rotation)
        cols = 100
        rows = 100
        z = np.ones((rows, cols))
        item.setData(z=z)
        return item

