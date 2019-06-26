from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from app.colors import *
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap
import os
# -- My Packages --
from ...inner_dock import InnerDock
from app.pyqt_frequently_used import create_param_combobox
from app.activation_b import btn


class SettingsDock(InnerDock):
    def __init__(self, main_layout):
        super().__init__(
            main_layout, 'Settings', b_pos=(0, 0), toggle_button=True,
            size=(1, 1))
        self.main_layout = main_layout
        self.create_settings_dock()

    def create_settings_dock(self):
        # Stop/Start button
        self.create_buttons()
        self.create_polycortex_label()
        # Plot parameter
        self.create_all_combobox()

    def create_all_combobox(self):
        create_param_combobox(
            self.layout, 'Vertical scale', (0, 1),
            ['Auto', '10 uv', '100 uv', '1000 uv', '10000 uv', '100000 uv'])
            # conn_func=self.main_eeg_dock.scale_y_axis)
        create_param_combobox(
            self.layout, 'Horizontal scale', (0, 2), ['5s', '7s', '10s'],
            editable=False)
        create_param_combobox(
            self.layout, 'Nb of columns', (0, 3), ['1', '2', '4'],
            editable=False)
            # conn_func=self.main_eeg_dock.change_num_plot_per_row
        create_param_combobox(
            self.layout, 'Aliasing', (0, 4), ['on', 'off'],
            editable=False)
            # , conn_func=self.start_aliasing

    def create_buttons(self):
        """Assign pushbutton for starting"""
        btn('Start', self.layout, (0, 0), toggle=True, max_width=100,
            color=dark_blue_tab, txt_color=white)
        # func_conn=self.main_eeg_dock.start_timers

    def create_polycortex_label(self):
        polycortex_label = QLabel()
        print(os.getcwd())
        polycortex_name_img = QPixmap(
            './GUI/img/polycortex_name_alpha_background.png')
        polycortex_label.setPixmap(polycortex_name_img)
        self.layout.addWidget(polycortex_label, 1, 0, 1, 1)

    def start_aliasing(self, txt):  # Need to do it before creating the graph
        # (don't work here but work when called in the main at the start)
        # Make it look WAY better but it is a bit more laggy, set it as a setting that can be activated
        if txt == 'on':
            pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
        elif txt == 'off':
            pg.setConfigOptions(antialias=False)
