# -- General Packages --
from pyqtgraph.dockarea import *
import pyqtgraph as pg
import numpy as np
import pyqtgraph.opengl as gl
# -- My packages --
from app.colors import *

class BasicP300:
    def __init__(self, area, below_dock):
        self.name = 'Basic P300'

        self.init_dock(area, below_dock)

    def init_dock(self, area, below_dock):
        dock = Dock(self.name)
        area.addDock(dock, 'above', below_dock)

        # layout = pg.LayoutWidget()
        # dock.addWidget(layout)

        self.w = self.init_win()
        dock.addWidget(self.w, 0, 0)

        self.add_rectangles()

    def init_win(self):
        w = gl.GLViewWidget()
        w.opts['distance'] = 20
        # w.opts['fov'] = 200
        w.opts['elevation'] = 0
        w.opts['azimuth'] = 0
        g = gl.GLGridItem()
        w.addItem(g)
        # plot = pg.PlotWidget()
        # sp = pg.ScatterPlotItem()
        # plot.addItem(sp)
        # plot.setYRange(0, 10)
        # plot.setXRange(0, 10)
        # plot.plotItem.hideAxis('bottom')
        # plot.plotItem.hideAxis('left')
        return w

    def add_rectangles(self):
        # verts = [[0, 0, 0], [0, 0, 10], [10, 0, 10], [10, 0, 10], [0, 10, 0], [0, 10, 10], [10, 0, 10], [10, 10, 10]]
        # verts = [[[0, 0, 0], [0, 0, 10], [10, 0, 10], [10, 0, 10]]]
        s_mesh = gl.MeshData.sphere(2, 2)
        s_item = gl.GLMeshItem(meshdata=s_mesh)

        self.w.addItem(s_item)
        
    def cube(self, rows, cols, radius=[1.0, 1.0], length=1.0, offset=False):
        """
        Return a MeshData instance with vertexes and faces computed
        for a cube surface.
        """

        verts = np.empty((rows+1, cols, 3), dtype=float)
        ## compute faces
        faces = np.empty((rows * cols * 2, 3), dtype=np.uint)


        return MeshData(vertexes=verts, faces=faces)
