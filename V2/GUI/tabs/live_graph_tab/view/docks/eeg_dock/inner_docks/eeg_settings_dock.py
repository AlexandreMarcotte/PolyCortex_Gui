from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QFont, QColor, QPen
from PyQt5.QtCore import QObject, Qt, pyqtSignal
# -- My Packages --
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
            self.inner_layout, 'Vertical scale', (0, 1),
            ['Auto', '10 uv', '100 uv', '1000 uv', '10000 uv', '100000 uv'])
        self.horizontal_scale_cb = ParameterCombobox(
            self.inner_layout, 'Horizontal scale', (0, 2), ['5s', '7s', '10s'],
            editable=False)
        self.nb_columns_cb = ParameterCombobox(
            self.inner_layout, 'Nb of columns', (0, 3), ['1', '2', '4'],
            editable=False)
        self.aliasing_cb = ParameterCombobox(
            self.inner_layout, 'Aliasing', (0, 4), ['on', 'off'],
            editable=False)

    def _create_polycortex_label(self):
        polycortex_label = QLabel()
        polycortex_name_img = QPixmap(
                './GUI/img/polycortex_name_alpha_background.png')
        polycortex_label.setPixmap(polycortex_name_img)
        self.inner_layout.addWidget(polycortex_label, 1, 0, 1, 1)
