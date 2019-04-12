from tabs.live_graph_tab.dock.inner_dock import InnerDock
from app.pyqt_frequently_used import create_param_combobox
from app.activation_b import btn
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from app.colors import *
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap
# -- My Packages --


class SettingsDock:
    def __init__(self, main_eeg_dock):
        self.main_eeg_dock = main_eeg_dock
        self.create_settings_dock()

    def create_settings_dock(self):
        settings_d = InnerDock(
            self.main_eeg_dock.layout, 'Settings', b_pos=(0, 1),toggle_button=True,
            size=(1, 1))
        # Stop/Start button
        self.create_buttons(settings_d.layout)
        self.create_polycortex_label(settings_d.layout)
        # Plot parameter
        self.create_all_combobox(settings_d.layout)
        self.main_eeg_dock.dock_area.addDock(settings_d.dock)

    def create_all_combobox(self, start_stop_l):
        create_param_combobox(
            start_stop_l, 'Vertical scale', (0, 1),
            ['Auto', '10 uv', '100 uv', '1000 uv', '10000 uv', '100000 uv'],
            conn_func=self.main_eeg_dock.scale_y_axis)
        create_param_combobox(
            start_stop_l, 'Horizontal scale', (0, 2), ['5s', '7s', '10s'],
            editable=False)
        create_param_combobox(
            start_stop_l, 'Nb of columns', (0, 3), ['1', '2', '4'],
            editable=False, conn_func=self.main_eeg_dock.change_num_plot_per_row)
        create_param_combobox(
            start_stop_l, 'Aliasing', (0, 4), ['on', 'off'],
            editable=False, conn_func=self.start_aliasing)

    def create_buttons(self, layout):
        """Assign pushbutton for starting"""
        btn('Start', layout, (0, 0), toggle=True, max_width=100,
            func_conn=self.main_eeg_dock.start_timers, color=dark_blue_tab,
            txt_color=white)

    def create_polycortex_label(self, layout):
        polycortex_label = QLabel()
        polycortex_name_image = QPixmap(
                './img/polycortex_name_alpha_background.png')
        polycortex_label.setPixmap(polycortex_name_image)
        layout.addWidget(polycortex_label, 1, 0, 1, 1)

    def start_aliasing(self, txt):  # Need to do it before creating the graph
        # (don't work here but work when called in the main at the start)
        # Make it look WAY better but it is a bit more laggy, set it as a setting that can be activated
        if txt == 'on':
            pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
        elif txt == 'off':
            pg.setConfigOptions(antialias=False)

