from app.colors import *
import pyqtgraph as pg
from abc import abstractclassmethod
# -- My Packages --
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from app.activation_b import btn


class SettingsDock(InnerDock):
    def __init__(self, main_layout):
        super().__init__(main_layout=main_layout, name='Settings')
        self.main_layout = main_layout
        self._create_settings_dock()

    def _create_settings_dock(self):
        # Stop/Start button
        self._create_start_buttons()

    def _create_start_buttons(self):
        """Assign pushbutton for starting"""
        self.start_btn = btn('Start', self.layout, toggle=True)

    @abstractclassmethod
    def _create_all_combobox(self):
        """Overload this method to create the combobox to act on the dock graph"""

    def start_aliasing(self, txt):  # Need to do it before creating the graph
        # (don't work here but work when called in the main at the start)
        # Make it look WAY better but it is a bit more laggy, set it as a setting that can be activated
        if txt == 'on':
            pg.setConfigOptions(antialias=True)  # Look at how much it change the performances
        elif txt == 'off':
            pg.setConfigOptions(antialias=False)


