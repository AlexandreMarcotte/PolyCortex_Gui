# --General Packages--
import pyqtgraph.opengl as gl
import numpy as np
# -- My Packages--
from .moving_object import MovingObject


class Sphere(MovingObject):
    def __init__(
            self, gv, scaling_factor=48, rows=10, cols=10,
            listening_process=False, update_func_name='move_pointer'):
        self.item = self.create_item(rows, cols, scaling_factor)
        super().__init__(gv, listening_process)
        self.radius = 1
        self.radius *= scaling_factor
        update_funcs = {'move_pointer': self.move_pointer,
                        'follow_plane': self.follow_plane}
        self.timer = self.create_timer(update_funcs[update_func_name])
        self.pos = np.array([0, 0, 0], dtype='float64')

    def set_element_to_follow(self, ele_to_follow):
        self.ele_to_follow = ele_to_follow

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

    def follow_plane(self):
        x = self.ele_to_follow[0][0]
        y = self.ele_to_follow[1][1]
        z = self.ele_to_follow[2][2]                                           # TODO: ALEXM: Abstract that into the class
                                                                               # TODO: make a class that contain the tree planes
        mvt = np.array([x, y, z]) - self.pos
        self.pos += mvt
        self.item.translate(*mvt)






