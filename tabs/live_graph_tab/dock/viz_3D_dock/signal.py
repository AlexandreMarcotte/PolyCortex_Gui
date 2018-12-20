# --General Packages--
import pyqtgraph.opengl as gl
import numpy as np
# TODO: ALEXM: inherit from GLLINEPLOTITEM Instead?
# --My Packages--
from .moving_object import MovingObject


class Signal(MovingObject):
    def __init__(self, gv, ch, listening_process=True, keys={'u':1, 'i':-1},
                 triplet_angle=None):
        super().__init__(gv, listening_process)
        self.gv = gv
        self.ch = ch
        self.keys= keys
        self.triplet_angle = triplet_angle

        self.line = gl.GLLinePlotItem()
        self.pos = np.array([0, 0, 0], dtype='float64')
        self.rot_mvt = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}

        self.timer = self.create_timer(self.rotate)

    def move(self, location=(0, 0, 0)):                                       # TODO: ALEXM: Use the local=True instead?
        mvt = np.array(location) - self.pos
        self.pos += mvt
        self.line.translate(*mvt)

    def rotate(self):
        if self.key_pressed in self.keys and self.ch == self.gv.ch_to_move:
            angle = self.keys[self.key_pressed] * 0.4
            mvt = self.rot_mvt[self.gv.rotation_axis]
            self.line.rotate(angle, *mvt, local=True)
