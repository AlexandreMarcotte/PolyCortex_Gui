# --General Packages--
import pyqtgraph.opengl as gl
import numpy as np
# from .moving_object import MovingObject


class Plane(gl.GLVolumeItem):
    def __init__(
                self, axis='x', mvt=np.array([1, 0, 0]), key=('j', 'k'),
                rotation=(0, 1, 0, 0), scale=1, mvt_scale=0.3,
                color=(255, 0, 0, 10), listening_process=True,
                triplet_box=None):
        self._cols = 150
        self._rows = 150
        plane_arr = np.empty((self._cols, self._rows, 1) + (4,), dtype=float)
        plane_arr[:, :] = color
        super().__init__(data=plane_arr, sliceDensity=10, smooth=True)
        # super().__init__(gv, listening_process)
        # variables for move_planes
        self._axis = axis
        self._mvt = mvt
        self._key = key
        self._mvt_scale = mvt_scale
        self._triplet_box = triplet_box
        self._planes = {'x': 0, 'y': 1, 'z': 2}

        self._rotation = rotation
        self._scale = scale
        self._color = color

        self._pos = np.array([0, 0, 0], dtype='float64')
        self._init_plane_item()

        # self.timer = self.create_timer(self.move_plane)

    def _init_plane_item(self):
        self.scale(self._scale, self._scale, 1)
        # center the init position
        init_pos = np.array([-self._cols//2, -self._rows//2, 0])
        # self.pos += mvt
        self.translate(*init_pos)
        self.rotate(*self._rotation)

    def move_plane(self):
        try:
            if self._axis == self.gv.plane_to_move:
                if self.key_pressed == self._key[0]:
                    mvt = self._mvt_scale * self._mvt
                    self.pos += mvt
                    self.translate(*mvt)
                if self.key_pressed == self._key[1]:
                    mvt = -1 * self._mvt_scale * self._mvt
                    self.pos += mvt
                    self.translate(*mvt)

            triplet_box_num = self._planes[self._axis]
            self._triplet_box.all_l_e[triplet_box_num].setText(
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


