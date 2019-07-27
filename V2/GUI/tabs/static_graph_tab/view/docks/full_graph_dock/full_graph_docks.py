from V2.GUI.tabs.inner_dock import InnerDock
from .full_graph_dock import FullGraphDock
from V2.general_settings import GeneralSettings


class FullGraphDocks(InnerDock):
    def __init__(self):
        super().__init__(
            'Full Graph', toggle_btn=False, add_dock_area=True,
            hide_title=False, set_scroll=True)
        for ch in range(GeneralSettings.N_CH):
            self.dock_area.addDock(FullGraphDock(ch))

