# --General packages--
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore
from pynput import keyboard
# -- My packages --
from app.colors import *
from app.activation_b import btn
from ... dock.dock import Dock
# To draw the brain
from .object_3D_creator import Obj3DCreator
from PyQt5 import QtGui
from save.data_saver import DataSaver
from .sphere import Sphere
from .brain import Brain
from .plane import Plane
from app.pyqt_frequently_used import (create_gr, create_txt_label,
                                      create_splitter, create_param_combobox,
                                      add_triplet_txt_box)

class Viz3D(Dock):
    def __init__(self, gv, layout):
        super().__init__(gv, layout, 'viz', 'Viz3D')
        self.gv = gv
        self.layout = layout

        self.len_sig = 100

        self.viz_layout, self.viz_gr = self.init_viz_layout()
        self.modify_curve_layout, self.modify_curve_gr = \
            self.init_modify_curve_layout()
        self.init_layout()
        # Create pointer sphere
        self.pointer_sphere = Sphere(
            scaling_factor=2, rows=10, cols=10, listening_process=True,
            update_func='move pointer')

        self.create_planes()

        self.sphere = Sphere(
            scaling_factor=48, rows=20, cols=20)
        # self.view.addItem(self.sphere.item)

        # self.create_total_brain()

        self.line_item = {}
        self.create_plot_lines()

        # self.on_off_button()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def create_planes(self):
        self.view.addItem(self.pointer_sphere.item)
        plane_z = Plane(color=(0, 0, 0.4, 0.5))
        plane_y = Plane(rotation=(90, 1, 0, 0), color=(0.4, 0, 0, 0.5))
        plane_x = Plane(rotation=(90, 0, 1, 0), color=(0, 0.4, 0, 0.5))
        self.view.addItem(plane_z.item)
        self.view.addItem(plane_y.item)
        self.view.addItem(plane_x.item)

    def create_grid(self, rotation=(0, 1, 0, 0),  scale=2):
        grid = gl.GLGridItem(size=QtGui.QVector3D(30,30,1))
        grid.scale(scale, scale, 1)
        if rotation[0]:
            grid.rotate(*rotation)
        return grid

    def init_viz_layout(self):
        viz_gr, viz_layout = create_gr()
        self.view = self.init_view()
        viz_layout.addWidget(self.view, 1, 0)
        return viz_layout, viz_gr

    def init_modify_curve_layout(self):
        modify_curve_gr, modify_curve_layout = create_gr()
        create_param_combobox(
            modify_curve_layout, 'Channel to modify', (0, 0, 1, 3),               # TODO: ALEXM: change to have a hboxlayout instead of a qboxlayout
            [str(ch) for ch in range(self.gv.N_CH)], self.print_shit, cols=3)
        # Position
        pos_l = create_txt_label('Position')
        add_triplet_txt_box(line=4, layout=modify_curve_layout)
        modify_curve_layout.addWidget(pos_l, 3, 0, 1, 3)
        # Angle
        angle_l = create_txt_label('Angle')
        modify_curve_layout.addWidget(angle_l, 5, 0, 1, 3)
        # Color
        color_l = create_txt_label('Color')
        add_triplet_txt_box(line=6, layout=modify_curve_layout)
        modify_curve_layout.addWidget(color_l, 7, 0, 1, 3)
        color_b = self.init_color_button()
        modify_curve_layout.addWidget(color_b, 8, 0, 1, 3)
        # Save to file
        data_saver = DataSaver(
            self.gv.main_window, self.gv, modify_curve_layout,
            saving_type='curve 3D pos save', pos=(9, 0), size=(1, 3),
            save_file_button=False, choose_b_size=(1, 3))
        return modify_curve_layout, modify_curve_gr

    def init_color_button(self):
        color_b = pg.ColorButton(close_fit=True)
        color_b.sigColorChanging.connect(self.print_shit)
        color_b.sigColorChanged.connect(self.print_shit)
        return color_b

    def print_shit(self):
        print('shizzle')

    def init_layout(self):
        self.init_on_off_button()
        splitter = create_splitter(self.viz_gr, self.modify_curve_gr)
        self.layout.addWidget(splitter, 0, 0)

    def create_total_brain(self):
        self.brain_v = Brain()
        self.brain_v.volume(show_box=False, show_axis=False)
        self.view.addItem(self.brain_v.volume)
        self.brain_s = Brain()
        self.brain_s.scatter()
        self.view.addItem(self.brain_s.volume)

    def create_plot_lines(self):
        for n in range(self.gv.N_CH):
            self.line_item[n] = gl.GLLinePlotItem()
            self.view.addItem(self.line_item[n])
            self.line_item[n].translate(-self.len_sig - self.sphere.radius, 0, 0)
            print('pos', self.line_item[n].pos)
            self.line_item[n].rotate(20*(n+1), 0, 1, 0)

    def init_view(self):
        """     """
        view = gl.GLViewWidget()
        view.opts['distance'] = 300
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view

    def set_plotdata(self, name, points, color, width):
        self.line_item[name].setData(pos=points, color=color, width=width)

    def update(self):
        for ch in range(self.gv.N_CH):
            pts = np.stack((np.linspace(0, self.len_sig, self.gv.DEQUE_LEN),
                            np.zeros(self.gv.DEQUE_LEN),
                            np.array(np.array(self.gv.data_queue[ch])/7000)), axis=1)

            self.set_plotdata(
                name=ch, points=pts, color=pg.glColor((ch, 8)), width=1)

    def init_on_off_button(self):
        btn('Start visualization 3D', self.viz_layout, (0, 0), func_conn=self.start,
            color=blue_b, toggle=True, txt_color=white, min_width=380)

    @QtCore.pyqtSlot(bool)
    def start(self, checked):
        if checked:
            self.timer.start(10)
            # self.brain_v.timer.start(10)
            self.pointer_sphere.timer.start(10)
        else:
            self.timer.stop()
            # self.brain_v.timer.stop()
            self.pointer_sphere.timer.stop()

