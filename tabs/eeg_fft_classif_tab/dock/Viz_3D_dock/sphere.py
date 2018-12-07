# --General Packages--
import pyqtgraph.opengl as gl
# -- My Packages--
from .moving_object import MovingObject


class Sphere(MovingObject):
    def __init__(self, scaling_factor=48, rows=20, cols=20,
                 update_func='update pos', listening_process=False):
        self.item = self.create_item(rows, cols, scaling_factor)

        super().__init__(self, update_func, listening_process)

        self.update_func = update_func

        self.key_pressed = ''

        self.radius = 1
        self.radius *= scaling_factor

    def create_item(self, rows, cols, scaling_factor):
        mesh = gl.MeshData.sphere(rows=rows, cols=cols)
        item = gl.GLMeshItem(
            meshdata=mesh, smooth=True, color=(1, 0, 0, 0.2),
            shader='shaded', glOptions='opaque')
        item.scale(scaling_factor, scaling_factor, scaling_factor)
        return item




