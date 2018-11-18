# -- General Packages --
from PyQt5.QtCore import Qt, pyqtSlot
from pyqtgraph.dockarea import *
import pyqtgraph as pg
import pyqtgraph.opengl as gl              # => Try to use pyopengl directly
# from OpenGL.GL import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from functools import partial
import numpy as np
# -- My packages --
from app.colors import *

#
# from pyqtgraph.Qt import QtCore, QtGui
# import pyqtgraph as pg
# import pyqtgraph.opengl as gl
#
# app = QtGui.QApplication([])
# w = gl.GLViewWidget()
# w.show()
# w.setWindowTitle('pyqtgraph example: GL Shaders')
# w.setCameraPosition(distance=15, azimuth=-90)


class BasicP300:
    def __init__(self, area, below_dock):
        self.name = 'Basic P300'
        self.area = area
        self.below_dock = below_dock
        self.init_dock()

    def init_dock(self):
        self.dock = Dock(self.name)
        self.area.addDock(self.dock, 'above', self.below_dock)
        Experiment(self.dock)


class Experiment:
    def __init__(self, dock):
        self.dock = dock

        self.w = self.init_win()
        self.add_rectangles()
        self.dock.addWidget(self.w, 1, 0, 1, 2)

        self.init_timer()
        self.add_start_button()
        self.add_stop_button()

    def init_win(self):
        w = gl.GLViewWidget()
        w.opts['distance'] = 15
        # w.opts['fov'] = 200
        w.opts['elevation'] = 0
        w.opts['azimuth'] = -90
        return w

    def add_rectangles(self):
        for x in range(1):
            pyramid = self.pyramid(pos=(x, 0, 0), s=(10, 10, 10))
            self.w.addItem(pyramid)
        # self.w.addItem(axis)
        g = gl.GLGridItem()
        self.w.addItem(g)

    def axis(self):
        axis = np.ones((10, 10, 10))
        axis = gl.GLVolumeItem(axis)
        return axis

    def cube(self, s=(1,1,1), pos=(0, 0, 0)):
        """
        Return a MeshData instance with vertexes and faces computed
        for a cube surface.
        """
        x, y, z = pos
        sx, sy, sz = s

        verts = np.array([
            np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), np.array([1, 0, 0]),
            np.array([0, 0, 1]), np.array([0, 1, 1]), np.array([1, 1, 1]), np.array([1, 0, 1])],
            dtype=float)

        # Resize:
        for v in verts:
            v[0] *= sx
            v[1] *= sy
            v[2] *= sz

        # Move:
        for v in verts:
            v[0] += x
            v[1] += y
            v[2] += z

        faces = np.array([
            np.array([0, 1, 2]), np.array([0, 3, 2]),
            np.array([4, 5, 6]), np.array([4, 7, 6]),
            np.array([0, 4, 7]), np.array([0, 3, 7]),
            np.array([1, 5, 6]), np.array([1, 2, 6]),
            np.array([0, 4, 5]), np.array([0, 1, 5]),
            np.array([3, 7, 6]), np.array([3, 2, 6])])

        cube = gl.MeshData(vertexes=verts, faces=faces)
        # cube = gl.MeshData.sphere(rows=2, cols=3)
        cube = gl.GLMeshItem(
            meshdata=cube, color=(0, 200, 0, 200), shader='shaded')

        # md = gl.MeshData.sphere(rows=20, cols=30)
        # m4 = gl.GLMeshItem(meshdata=md, smooth=True, shader='shaded', glOptions='opaque')
        # w.addItem(m4)

        return cube

    def pyramid(self, s=(1,1,1), pos=(0, 0, 0)):
        """
        Return a MeshData instance with vertexes and faces computed
        for a cube surface.
        """
        x, y, z = pos
        sx, sy, sz = s

        verts = np.array([
            np.array([0.5, 0.5, 1]),
            np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), np.array([1, 0, 0])],
            dtype=float)

        # Resize:
        for v in verts:
            v[0] *= sx
            v[1] *= sy
            v[2] *= sz

        # Move:
        for v in verts:
            v[0] += x
            v[1] += y
            v[2] += z

        faces = np.array([
            np.array([0, 1, 2]), np.array([0, 3, 2]), np.array([0, 4, 3]), np.array([0, 1, 4])])

        pyramid = gl.MeshData(vertexes=verts, faces=faces)
        # cube = gl.MeshData.sphere(rows=2, cols=3)
        pyramid = gl.GLMeshItem(
            meshdata=pyramid, color=(0, 200, 0, 200), shader='shaded')

        # md = gl.MeshData.sphere(rows=20, cols=30)
        # m4 = gl.GLMeshItem(meshdata=md, smooth=True, shader='shaded', glOptions='opaque')
        # w.addItem(m4)

        return pyramid

    def init_timer(self):
        self.timer_effect = QtCore.QTimer()
        self.timer_effect.timeout.connect(self.update_display)
        self.timer_effect.start(1000)

    def update_display(self):
        # print('hooouuuinnnn ')
        pass
    def add_start_button(self):
        b_start = QtGui.QPushButton('START P300')
        b_start.setStyleSheet("background-color: rgba(255, 255, 255, 0.5)")
        b_start.clicked.connect(partial(self.start_p300))
        self.dock.addWidget(b_start, 0, 0)

    @pyqtSlot()
    def start_p300(self):
        self.timer_effect.start(200)

    def add_stop_button(self):
        b_stop = QtGui.QPushButton('STOP P300')
        b_stop.setStyleSheet("background-color: rgba(0, 0, 0, 0.5)")
        b_stop.clicked.connect(partial(self.stop_p300))
        self.dock.addWidget(b_stop, 0, 1)

    @pyqtSlot()
    def stop_p300(self):
        self.timer_effect.stop()

