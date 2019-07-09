from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from app.colors import *
import pyqtgraph as pg
from PyQt5.QtGui import QPixmap
import os
# -- My Packages --
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from app.pyqt_frequently_used import create_param_combobox
from app.activation_b import btn
from V2.utils.parameter_combobox import ParameterCombobox
from V2.GUI.tabs.live_graph_tab.view.docks.inner_docks.settings_dock import SettingsDock


class EegSettingsDock(SettingsDock):
    def __init__(self, main_layout):
        super().__init__(main_layout)

        self.main_layout = main_layout

        self._create_settings_dock()

    def _create_settings_dock(self):
        super()._create_settings_dock()
        # Plot parameter
        self._create_all_combobox()
        # Polycortex label
        self._create_polycortex_label()

    def _create_all_combobox(self):
        self.vertical_scale_cb = ParameterCombobox(
            self.layout, 'Vertical scale', (0, 1),
            ['Auto', '10 uv', '100 uv', '1000 uv', '10000 uv', '100000 uv'])
        # conn_func=self.main_eeg_dock.scale_y_axis)
        self.horizontal_scale_cb = ParameterCombobox(
            self.layout, 'Horizontal scale', (0, 2), ['5s', '7s', '10s'],
            editable=False)
        self.nb_columns_cb = ParameterCombobox(
            self.layout, 'Nb of columns', (0, 3), ['1', '2', '4'],
            editable=False)
        # conn_func=self.main_eeg_dock.change_num_plot_per_row
        self.aliasing_cb = ParameterCombobox(
            self.layout, 'Aliasing', (0, 4), ['on', 'off'],
            editable=False)
        # , conn_func=self.start_aliasing
        # print('cool')

    def _create_polycortex_label(self):
        polycortex_label = QLabel()
        polycortex_name_img = QPixmap(
            './GUI/img/polycortex_name_alpha_background.png')
        polycortex_label.setPixmap(polycortex_name_img)
        self.layout.addWidget(polycortex_label, 1, 0, 1, 1)
