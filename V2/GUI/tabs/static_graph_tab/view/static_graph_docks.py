# -- General Packages --
from typing import List
# -- My Packages --
from V2.GUI.tabs.inner_dock import InnerDock
from V2.general_settings import GeneralSettings


class StaticGraphDocks(InnerDock):
    def __init__(self, name, size):
        super().__init__(
            name, toggle_btn=False, add_dock_area=True,
            hide_title=False, size=size)

    def _init_docks(self, dock_type):
        self.docks: List[dock_type] = []
        for ch in range(GeneralSettings.N_CH):
            dock = dock_type(ch)
            self.docks.append(dock)
            self.dock_area.addDock(dock)

    def update_signals(self, signals_matrix):
        for ch, dock in enumerate(self.docks):
            dock.update(signals_matrix[:, ch])
