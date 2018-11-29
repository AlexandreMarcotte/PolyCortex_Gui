# --General packages--
from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
# -- My packages --
from app.colors import *
from app.activation_b import btn
from PyQt5 import QtCore
from random import randrange
# To draw the brain
from tabs.brain_3D_tab.brain_3D_tab import Obj3DCreator


class Viz3D:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        self.len_sig = 100

        self.view = self.init_view()
        self.layout.addWidget(self.view, 1, 0)

        self.sphere = Sphere()
        # self.view.addItem(self.sphere.item)

        # self.create_total_brain()
        #
        self.traces = {}
        self.create_plot_lines()

        self.on_off_button()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def create_total_brain(self):
        self.brain_v = Brain()
        self.brain_v.volume()
        self.view.addItem(self.brain_v.volume)
        self.brain_s = Brain()
        self.brain_s.scatter()
        self.view.addItem(self.brain_s.volume)

    def create_plot_lines(self):
        for n in range(self.gv.N_CH):
            self.traces[n] = gl.GLLinePlotItem()
            self.view.addItem(self.traces[n])
            self.traces[n].translate(-self.len_sig - self.sphere.radius, 0, 0)
            self.traces[n].rotate(20*(n+1), 0, 1, 0)

    def init_view(self):
        """     """
        view = gl.GLViewWidget()
        # view.opts['center'] = QtGui.QVector3D(0, 230000, 0)
        view.opts['distance'] = 300
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view

    def set_plotdata(self, name, points, color, width):
        self.traces[name].setData(pos=points, color=color, width=width)

    def update(self):
        for ch in range(self.gv.N_CH):
            pts = np.stack((np.linspace(0, self.len_sig, self.gv.DEQUE_LEN),
                            np.zeros(self.gv.DEQUE_LEN),
                            np.array(np.array(self.gv.data_queue[ch])/7000)), axis=1)

            self.set_plotdata(
                name=ch, points=pts, color=pg.glColor((ch, 8)), width=1)

    def on_off_button(self):
        btn('Start visualization 3D', self.layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(10)
            # self.brain_v.timer.start(10)
            # self.sphere.timer.start(10)
        else:
            self.timer.stop()
            # self.brain_v.timer.stop()
            # self.sphere.timer.stop()


class Sphere:
    def __init__(self):
        self.mesh = gl.MeshData.sphere(rows=20, cols=20)
        self.radius = 1
        self.scaling_factor = 48
        self.radius *= self.scaling_factor

        self.item = gl.GLMeshItem(
            meshdata=self.mesh, smooth=False, shader='normalColor', glOptions='opaque')
        # self.m2.translate(self.x_pos, self.y_pos, self.character_height)
        self.item.scale(self.scaling_factor, self.scaling_factor, self.scaling_factor)
        self.create_timer()

    def create_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_pos)

    def update_pos(self):
        # self.item.translate(1000, 0, 0)
        pass


class Brain:
    def __init__(self):
        self.obj_3d_creator = Obj3DCreator()

        self.create_timer()
        self.i = 0

    def scatter(self):
        self.volume = self.obj_3d_creator.create_3D_scatter_plot()

    def volume(self):
        self.volume = self.obj_3d_creator.create_3D_brain_volume(
            scale=1, show_box=False, show_axis=False)

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
