# --General Packages--
import pyqtgraph.opengl as gl
# -- My Packages--
from .moving_object import MovingObject


class Sphere(MovingObject):
    def __init__(
                self, gv, scaling_factor=48, rows=20, cols=20,
                update_func='update pos', listening_process=False):
        self.item = self.create_item(rows, cols, scaling_factor)

        super().__init__(gv, listening_process)

        self.update_func = update_func


        self.radius = 1
        self.radius *= scaling_factor

        self.create_timer(self.move_pointer)

    def create_item(self, rows, cols, scaling_factor):
        mesh = gl.MeshData.sphere(rows=rows, cols=cols)
        item = gl.GLMeshItem(
                meshdata=mesh, smooth=True, color=(1, 0, 0, 0.2),
                shader='shaded', glOptions='opaque')
        item.scale(scaling_factor, scaling_factor, scaling_factor)
        return item

    def move_pointer(self):
        try:
            mvt = self.pointer_actn[self.key_pressed]
            self.item.translate(mvt[0], mvt[1], mvt[2])
            self.pos += mvt
        except KeyError:
            pass




