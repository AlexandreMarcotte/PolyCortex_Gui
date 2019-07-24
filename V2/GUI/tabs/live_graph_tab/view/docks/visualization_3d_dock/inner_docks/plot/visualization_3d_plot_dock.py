from pyqtgraph.dockarea import Dock
import numpy as np
from mne.surface import decimate_surface
import mne
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
# --My packages--
import pyqtgraph.opengl as gl
from .plane import Plane
from .sphere import Sphere
from .brain import Brain
from .read_nii_data import read_nii_data
from .signal import Signal
from V2.general_settings import GeneralSettings


class Visualization3dPlotsDock(Dock):
    def __init__(self):
        super().__init__(name='', hideTitle=True)

        self._gl_view = self._init_plot()

        self.N_CH = GeneralSettings.N_CH
        self.QUEUE_LEN = GeneralSettings.QUEUE_LEN
        self._init_planes()
        self._init_sphere()
        self._init_total_brain()
        self._init_head()
        self._init_signals_line_item()

        self.addWidget(self._gl_view)

        self._init_timer()

    def _init_signals_line_item(self):
        # Boundary sphere is use to place the distance of the signals
        self.signals_item = {}
        self.len_sig = 100
        self._boundary_sphere = Sphere(scaling_factor=48)
        self._create_plot_lines()

    def _init_timer(self):
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._update)

    @staticmethod
    def _init_plot():
        gl_view = gl.GLViewWidget()
        gl_view.opts['distance'] = 370
        gl_view.opts['azimuth'] = 40
        gl_view.opts['elevation'] = 15
        return gl_view

    def _init_planes(self):
        self.plane_x = Plane(
            axis='x', mvt=np.array([1, 0, 0]), key=('j', 'k'),
            rotation=(90, 0, 1, 0), color=(0, 0, 255, 4))
        self.plane_y = Plane(
            axis='y', mvt=np.array([0, 1, 0]), key=('j', 'k'),
            rotation=(90, 1, 0, 0), color=(0, 255, 0, 4))
        self.plane_z = Plane(
            axis='z', mvt=np.array([0, 0, 1]), key=('j', 'k'),
            color=(255, 0, 0, 4))
        # Add to view
        self._gl_view.addItem(self.plane_x)
        self._gl_view.addItem(self.plane_y)
        self._gl_view.addItem(self.plane_z)
        # Add to a list
        self._planes = [self.plane_x, self.plane_y, self.plane_z]

    def _init_sphere(self):
        self.electrod_sphere = Sphere(
            scaling_factor=3, update_func_name='follow_plane')
        self._gl_view.addItem(self.electrod_sphere)

    def _init_total_brain(self):
        brain_data = read_nii_data(
            nii_path='GUI/tabs/live_graph_tab/view/docks/visualization_3d_dock/inner_docks/plot/inplane001.nii')
        self.brain = Brain(brain_data)
        self._gl_view.addItem(self.brain.item)

    def _init_head(self):
        path = mne.datasets.sample.data_path()
        surf = mne.read_bem_surfaces(
            path + '/subjects/sample/bem/sample-head.fif')[0]
        points, triangles = surf['rr'], surf['tris']
        # reduce to 30000 triangles:
        points_dec, triangles_dec = decimate_surface(
            points, triangles, n_triangles=3000)
        p, t = points_dec, triangles_dec
        mesh_data = gl.MeshData(p, t)
        mesh_item = gl.GLMeshItem(
            meshdata=mesh_data, computeNormals=True,
            shader='viewNormalColor', glOptions='translucent')
        mesh_item.translate(0, 0, -20)
        mesh_item.rotate(90, 1, 0, 0)
        mesh_item.scale(650, 650, 650)
        mesh_item.setColor([0, 0, 1, 0.4])

        self._gl_view.addItem(mesh_item)

    def connect_signals(self, signals):
        self.signals = signals

    def _create_plot_lines(self):
        for n in range(self.N_CH):
            self.signals_item[n] = Signal(ch=n)
            self._gl_view.addItem(self.signals_item[n].line)
            self.signals_item[n].move(
                location=(-self.len_sig - self._boundary_sphere.radius, 0, 0))
            self.signals_item[n].line.rotate(20*(n+1), 0, 1, 0)

    def _set_plot_data(self, name, points, color, width):
        self.signals_item[name].line.setData(pos=points, color=color, width=width)

    def _update(self):
        for ch in range(self.N_CH):
            pts = np.stack((
                np.linspace(0, self.len_sig, self.QUEUE_LEN),
                np.zeros(self.QUEUE_LEN),
                np.array(np.array(self.signals[ch])/7000)),
                axis=1)

            self._set_plot_data(
                name=ch, points=pts, color=pg.glColor((ch, 8)), width=1)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        # if checked:
        self._timer.start(10)
        # self._electrod_sphere.timer.start(8)
        # for plane in self._planes:
        #     plane.timer.start(8)
        for signal in self.signals_item.values():
            signal.timer.start(8)
        # else:
        #     self.timer.stop()
        #     self.electrod_sphere.timer.stop()
        #     for plane in self.planes:
        #         plane.timer.stop()
        #     for signal in self.signals.values():
        #         signal.timer.stop()

