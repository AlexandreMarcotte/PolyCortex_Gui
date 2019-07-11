# -- My Packages --
from V2.utils.parameter_combobox import ParameterCombobox
from V2.GUI.tabs.live_graph_tab.view.docks.inner_docks.settings_dock import SettingsDock
from V2.utils.triplet_box import TripletBox
from V2.utils.colors import *
from V2.utils.data_saver import DataSaver
from V2.utils.btn import Btn


class Visualisation3dSettingsDock(SettingsDock):
    def __init__(self, main_layout):
        super().__init__(main_layout)
        self._create_settings_dock()

    def _create_settings_dock(self):
        super()._create_settings_dock()
        # Plot parameter
        self._create_all_combobox()

    def _create_all_combobox(self):
        self.ch_to_move_cb = ParameterCombobox(
            self.inner_layout, 'Ch to move', (0, 1),
            [str(ch + 1) for ch in range(8)])
        # Position
        self.pos_triplet_box = TripletBox(
            self.inner_layout, 'Position', (0, 2),
            colors=(blue_plane, green_plane, red_plane))
        # Angle
        self.pos_triplet_box = TripletBox(
            self.inner_layout, 'Angle', (0, 5),
            colors=(blue_plane, green_plane, red_plane))
        # Data saver
        self.data_saver = DataSaver(self.inner_layout, pos=(0, 8))
        # Show 3D
        self.show_3d_btn = Btn('Show 3D', color=grey3)
        self.inner_layout.addWidget(self.show_3d_btn, 1, 0)

