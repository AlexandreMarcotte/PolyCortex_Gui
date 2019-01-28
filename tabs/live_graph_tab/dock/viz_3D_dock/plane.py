# --General Packages--
import pyqtgraph.opengl as gl
import numpy as np
from .moving_object import MovingObject
from app.colors import *
from PyQt5.QtGui import QColor


class Plane(MovingObject):
    def __init__(
                self, gv, axis='x', mvt=np.array([1, 0, 0]), key=('j', 'k'),
                rotation=(0, 1, 0, 0), scale=1, mvt_scale=0.3,
                color=(255, 0, 0, 10), listening_process=True,
                triplet_box=None):

        self.gv = gv
        self.axis = axis
        self.mvt = mvt
        self.key = key
        self.mvt_scale = mvt_scale
        self.triplet_box = triplet_box
        super().__init__(gv, listening_process)
        self.rotation = rotation
        self.scale = scale
        self.color = color
        self.planes = {'x': 0, 'y': 1, 'z': 2}

        self.pos = np.array([0, 0, 0], dtype='float64')
        self.item = self.init_plane_item()

        self.timer = self.create_timer(self.move_plane)

    def init_plane_item(self):
        cols = 150
        rows = 150
        plane = np.empty((cols, rows, 1) + (4,), dtype=float)
        plane[:, :] = self.color
        item = gl.GLVolumeItem(plane, sliceDensity=5, smooth=True)
        item.scale(self.scale, self.scale, 1)
        init_pos = np.array([-cols//2, -rows//2, 0])
        # self.pos += mvt
        item.translate(*init_pos)
        item.rotate(*self.rotation)
        return item

    def move_plane(self):
        try:
            if self.axis == self.gv.plane_to_move:
                if self.key_pressed == self.key[0]:
                    mvt = self.mvt_scale * self.mvt
                    self.pos += mvt
                    self.item.translate(*mvt)
                if self.key_pressed == self.key[1]:
                    mvt = -1 * self.mvt_scale * self.mvt
                    self.pos += mvt
                    self.item.translate(*mvt)

            triplet_box_num = self.planes[self.axis]
            self.triplet_box.all_l_e[triplet_box_num].setText(
                    str(int(self.pos[triplet_box_num])))

        except KeyError as e:
            print(e)

    # def init_plane_item(self):                                               # TODO: ALEXM: Try again to use a plane with the technique I used with a head
    #     cols = 150
    #     rows = 150
    #     plane = np.empty((cols, rows, 1) + (4,), dtype=float)
    #     plane[:, :] = [0, 0, 255, 10]
    #     item = gl.GLSurfacePlotItem(plane, computeNormals=True, smooth=False)
    #     item.scale(self.scale, self.scale, 1)
    #     item.translate(-50, -50, 0)
    #     item.rotate(*self.rotation)
    #     x = np.linspace(-100, 100, cols).reshape(cols, 1)
        # y = np.linspace(-100, 100, rows).reshape(1, rows)
        # z = np.ones((rows, cols))
        # x = np.array([0, 100])
        # y = np.array([0, 100])
        # z = np.array([[(1,1,1), (1,1,1)], [(1,1,1), (1,1,1)]])
        # item.setColor(QColor('rgba(255, 255, 0, 50)'))
        # return item


