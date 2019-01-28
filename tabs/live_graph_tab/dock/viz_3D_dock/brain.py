# --General Packages--
from .object_3D_creator import Obj3DCreator
from random import randrange
from PyQt5 import QtCore


class Brain:
    def __init__(self):
        self.obj_3d_creator = Obj3DCreator()

        self.create_timer()
        self.i = 0

    def scatter(self):
        self.volume = self.obj_3d_creator.create_3D_scatter_plot()

    def volume(self, show_box=False, show_axis=False):
        self.volume = self.obj_3d_creator.create_3D_brain_volume(
            scale=1, show_box=show_box, show_axis=show_axis)

    def create_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_brain_pos)

    def update_brain_pos(self):
        self.i += 1
        print(self.i)
        # brain.translate(10000, 0, 0)
        x = randrange(100)
        y = randrange(100)
        z = randrange(100)
        self.obj_3d_creator.brain[x, y, z] = [255, 0, 0, 255]
        self.volume.setData(self.obj_3d_creator.brain)