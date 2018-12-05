# --General packages--
from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore
from random import randrange
from pynput import keyboard
# -- My packages --
from app.colors import *
from app.activation_b import btn
from ... dock.dock import Dock
# To draw the brain
from tabs.brain_3D_tab.brain_3D_tab import Obj3DCreator
from PyQt5 import QtGui
from save.data_saver import DataSaver


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
        grid_x = self.create_grid(scale=3)
        grid_y = self.create_grid(rotation=(90, 1, 0, 0), scale=3)
        grid_z = self.create_grid(rotation=(90, 0, 1, 0), scale=3)
        self.view.addItem(grid_x)
        self.view.addItem(grid_y)
        self.view.addItem(grid_z)

        self.sphere = Sphere(
            scaling_factor=48, rows=20, cols=20)
        # self.view.addItem(self.sphere.item)

        self.create_total_brain()

        self.line_item = {}
        self.create_plot_lines()

        # self.on_off_button()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def create_grid(self, rotation=(0, 1, 0, 0),  scale=2):
        grid = gl.GLGridItem(size=QtGui.QVector3D(30,30,1))
        grid.scale(scale, scale, 1)
        if rotation[0]:
            grid.rotate(*rotation)
        return grid

    def init_viz_layout(self):
        viz_gr, viz_layout = self.create_gr()
        self.view = self.init_view()
        viz_layout.addWidget(self.view, 1, 0)
        return viz_layout, viz_gr

    def init_modify_curve_layout(self):
        modify_curve_gr, modify_curve_layout = self.create_gr()
        self.create_param_combobox(
            modify_curve_layout, 'Channel to modify', (0, 0, 1, 3),               # TODO: ALEXM: change to have a hboxlayout instead of a qboxlayout
            [str(ch) for ch in range(self.gv.N_CH)], self.print_shit, cols=3)
        # Position
        pos_l = self.create_txt_label('Position')
        self.add_triplet_txt_box(line=4, layout=modify_curve_layout)
        modify_curve_layout.addWidget(pos_l, 3, 0, 1, 3)
        # Angle
        angle_l = self.create_txt_label('Angle')
        modify_curve_layout.addWidget(angle_l, 5, 0, 1, 3)
        # Color
        color_l = self.create_txt_label('Color')
        self.add_triplet_txt_box(line=6, layout=modify_curve_layout)
        modify_curve_layout.addWidget(color_l, 7, 0, 1, 3)
        color_b = pg.ColorButton()
        color_b.sigColorChanging.connect(self.print_shit)
        color_b.sigColorChanged.connect(self.print_shit)
        modify_curve_layout.addWidget(color_b, 8, 0, 1, 3)
        # Save to file
        data_saver = DataSaver(
            self.gv.main_window, self.gv, modify_curve_layout,
            saving_type='curve 3D pos save', pos=(9, 0), size=(1, 3),
            save_file_button=False, choose_b_size=(1, 3))
        return modify_curve_layout, modify_curve_gr

    def print_shit(self):
        print('shizzle')

    def init_layout(self):
        self.init_on_off_button()
        splitter = self.create_splitter(self.viz_gr, self.modify_curve_gr)
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
        # view.opts['center'] = QtGui.QVector3D(0, 230000, 0)
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
            color=blue_b, toggle=True, txt_color=white)

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


# class CurveItem:
#     def __init__(self, curve):
#         self.pos = [0, 0, 0]
#         self.curve = curve

class Sphere:
    def __init__(self, scaling_factor=48, rows=20, cols=20,
                 update_func='update_pos', listening_process=False):
        self.radius = 1
        self.scaling_factor = scaling_factor
        self.radius *= self.scaling_factor
        self.update_func = update_func

        self.key_pressed = 'a'

        self.mesh = gl.MeshData.sphere(rows=rows, cols=cols)
        self.item = gl.GLMeshItem(
            meshdata=self.mesh, smooth=True, color=(1, 0, 0, 0.2),
            shader='shaded', glOptions='opaque')
        self.item.scale(self.scaling_factor, self.scaling_factor, self.scaling_factor)
        self.create_timer()

        if listening_process:
            self.start_listening_process()
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0

    def start_listening_process(self):
        listen_keybr = keyboard.Listener(on_press=self.on_press,
                                         on_release=self.on_release)
        listen_keybr.start()

    def create_timer(self):
        self.timer = QtCore.QTimer()
        if self.update_func == 'update pos':
            self.timer.timeout.connect(self.update_func)
        elif self.update_func == 'move pointer':
            print('update_pointer')
            self.timer.timeout.connect(self.move_pointer)

    def update_pos(self):
        # self.item.translate(1000, 0, 0)
        pass

    def move_pointer(self):
        # X
        if self.key_pressed=='d':
            self.item.translate(0.2, 0, 0)
            self.x_pos += 0.2
        if self.key_pressed=='a':
            self.item.translate(-0.2, 0, 0)
            self.x_pos -= 0.2
        # Y
        if self.key_pressed=='s':
            self.item.translate(0, 0.3, 0)
            self.y_pos += 0.3
        if self.key_pressed=='w':
            self.item.translate(0,-0.3, 0)
            self.y_pos -= 0.3
        # Z
        if self.key_pressed=='r':
            self.item.translate(0, 0, 0.3)
            self.z_pos += 0.3
        if self.key_pressed=='f':
            self.item.translate(0, 0, -0.3)
            self.z_pos -= 0.3
        print('x: ', self.x_pos, 'y: ', self.y_pos, 'z: ', self.z_pos)

    def on_press(self, key):
        try:
            self.key_pressed = key.char
            print(self.key_pressed)
        except AttributeError:
            # print(f'special key {key} pressed')
            self.key_pressed = key

    def on_release(self, key):
        pass
        if key == keyboard.Key.esc:
            # Stop listener
            pass


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
