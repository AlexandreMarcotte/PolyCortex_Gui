# --General packages--
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import mne
from mne.surface import decimate_surface
from pyqtgraph.Qt import QtCore
from pyqtgraph.dockarea import *
# -- My packages --
from app.colors import *
from app.activation_b import btn
from ... dock.dock import Dock
# To draw the brain
from save.data_saver import DataSaver
from .sphere import Sphere
from .brain import Brain
from .plane import Plane
from .signal import Signal
from app.pyqt_frequently_used import (
        create_gr, create_txt_label, create_splitter, create_param_combobox,
        TripletBox)
from tabs.live_graph_tab.dock.inner_dock import InnerDock
from .read_nii_data import read_nii_data


class Viz3D(Dock):
    def __init__(self, gv, layout):
        secondary_gr, secondary_layout = create_gr()
        super().__init__(gv, 'viz', secondary_layout)
        self.gv = gv
        self.layout = layout

        self.dock_area = DockArea()
        self.layout.addWidget(self.dock_area, 1, 0, 1, 8)

        self.len_sig = 100

        self.init_modify_curve_layout()
        self.init_viz_layout()

        self.electrod_sphere = Sphere(
                self.gv, scaling_factor=3, update_func_name='follow_plane')
        self.view.addItem(self.electrod_sphere.item)

        self.planes = self.create_planes()
        self.planes_pos = [plane.pos for plane in self.planes]
        for plane in self.planes:
            self.view.addItem(plane.item)
        self.electrod_sphere.set_element_to_follow(
                ele_to_follow=self.planes_pos)

        self.sphere = Sphere(self.gv, scaling_factor=48)

        self.signals = {}
        self.create_plot_lines()

        # self.on_off_button()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def show_3D_viz_b(self, layout):
        btn('Show 3D', layout, (1, 0), func_conn=self.show_3D_viz, color=grey3,
            txt_color=white)

    def show_3D_viz(self):
        self.create_head()
        self.create_total_brain()

    def create_head(self):
        path = mne.datasets.sample.data_path()
        print('path', path)
        surf = mne.read_bem_surfaces(
                path + '/subjects/sample/bem/sample-head.fif')[0]
        points, triangles = surf['rr'], surf['tris']
        # reduce to 30000 triangles:
        points_dec, triangles_dec = decimate_surface(
                points, triangles, n_triangles=30000)
        p, t = points_dec, triangles_dec
        mesh_data = gl.MeshData(p, t)
        mesh_item = gl.GLMeshItem(
                meshdata=mesh_data, computeNormals=True,
                shader='viewNormalColor', glOptions='translucent')
        mesh_item.translate(0, 0, -20)
        mesh_item.rotate(90, 1, 0, 0)
        mesh_item.scale(650, 650, 650)
        mesh_item.setColor([0, 0, 1, 0.4])

        self.view.addItem(mesh_item)

    def create_planes(self):
        plane_x = Plane(
                self.gv, axis='x', mvt=np.array([1, 0, 0]), key=('j', 'k'),
                rotation=(90, 0, 1, 0), color=(0, 0, 255, 4),
                triplet_box=self.triplet_box)
        plane_y = Plane(
                self.gv, axis='y', mvt=np.array([0, 1, 0]), key=('j', 'k'),
                rotation=(90, 1, 0, 0), color=(0, 255, 0, 4),
                triplet_box=self.triplet_box)
        plane_z = Plane(
                self.gv, axis='z', mvt=np.array([0, 0, 1]), key=('j', 'k'),
                color=(255, 0, 0, 4), triplet_box=self.triplet_box)

        return plane_x, plane_y, plane_z

    def init_viz_layout(self):
        # viz_gr, viz_layout = create_gr()
        viz_d = InnerDock(self.layout, 'Visualization')
        self.view = self.init_view()
        viz_d.layout.addWidget(self.view)
        # self.layout.addWidget(self.view, 2, 0, 1, 9)
        self.dock_area.addDock(viz_d.dock)

    def init_modify_curve_layout(self):
        settings_d = InnerDock(
                self.layout, 'Settings', toggle_button=True, size=(1, 1))
        # Stop/Start button
        self.init_on_off_button(settings_d.layout)

        # modify_curve_gr, modify_curve_layout = create_gr()
        create_param_combobox(
                settings_d.layout, 'Ch to move', (0, 1, 1, 1),                 # TODO: ALEXM: change to have a hboxlayout instead of a qboxlayout
                [str(ch+1) for ch in range(self.gv.N_CH)],
                self.change_pos_and_angle_of_signal, cols=1, editable=False)
        # Position
        pos_l = create_txt_label('Position')
        settings_d.layout.addWidget(pos_l, 0, 2, 1, 3)
        self.triplet_box = TripletBox(
                self.gv, name='position', col=2, layout=settings_d.layout,
                colors=(blue_plane, green_plane, red_plane))
        # Angle
        angle_l = create_txt_label('Angle')
        settings_d.layout.addWidget(angle_l, 0, 5, 1, 3)
        self.triplet_angle = TripletBox(
                self.gv, name='angle', col=5, layout=settings_d.layout,
                colors=(blue_plane, green_plane, red_plane))
        # Save to file
        DataSaver(
                self.gv.main_window, self.gv, settings_d.layout,               # TODO: ALEXM: Add a tooltip
                saving_type='Save', pos=(0, 8), size=(1, 1),
                save_file_button=True, choose_b_size=(1, 1))
        # return modify_curve_layout, modify_curve_gr
        self.show_3D_viz_b(settings_d.layout)

        self.dock_area.addDock(settings_d.dock)

    def init_color_button(self):
        color_b = pg.ColorButton(close_fit=True)
        # color_b.sigColorChanging.connect(self.print_shit)
        # color_b.sigColorChanged.connect(self.print_shit)
        return color_b

    def print_shit(self):
        print('shizzle')

    def change_pos_and_angle_of_signal(self, ch_to_move):
        self.gv.ch_to_move = int(ch_to_move) - 1
        pos = self.planes_pos
        # print('The ch to move is: ', ch_to_move,
        #       'The position of the plane is: ', pos)
        self.signals[int(ch_to_move)-1].move(
            location=(pos[0][0], pos[1][1], pos[2][2]))

    def create_total_brain(self):
        brain_data = read_nii_data(
            nii_path='tabs/live_graph_tab/dock/viz_3D_dock/inplane001.nii')
        self.brain = Brain(brain_data, 'volume')
        self.view.addItem(self.brain.item)

    def create_plot_lines(self):
        for n in range(self.gv.N_CH):
            self.signals[n] = Signal(
                    self.gv, ch=n, triplet_angle=self.triplet_angle)
            self.view.addItem(self.signals[n].line)
            self.signals[n].move(
                location=(-self.len_sig - self.sphere.radius, 0, 0))
            self.signals[n].line.rotate(20*(n+1), 0, 1, 0)

    def init_view(self):
        """     """
        view = gl.GLViewWidget()
        view.opts['distance'] = 370
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view

    def set_plot_data(self, name, points, color, width):
        self.signals[name].line.setData(pos=points, color=color, width=width)

    def update(self):
        for ch in range(self.gv.N_CH):
            pts = np.stack((
                    np.linspace(0, self.len_sig, self.gv.DEQUE_LEN),
                    np.zeros(self.gv.DEQUE_LEN),
                    np.array(np.array(self.gv.data_queue[ch])/7000)),
                    axis=1)

            self.set_plot_data(
                    name=ch, points=pts, color=pg.glColor((ch, 8)), width=1)

    def init_on_off_button(self, layout=None):
        btn('Start', layout, (0, 0), func_conn=self.start, max_width=100,
            min_width=100, color=dark_blue_tab, toggle=True, txt_color=white)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(10)
            self.electrod_sphere.timer.start(8)
            for plane in self.planes:
                plane.timer.start(8)
            for signal in self.signals.values():
                signal.timer.start(8)
        else:
            self.timer.stop()
            self.electrod_sphere.timer.stop()
            for plane in self.planes:
                plane.timer.stop()
            for signal in self.signals.values():
                signal.timer.stop()

