from V2.GUI.tabs.inner_dock import InnerDock
from .portion_graph_dock import PortionGraphDock
from V2.general_settings import GeneralSettings


class PortionGraphDocks(InnerDock):
    def __init__(self):
        super().__init__(
            'Portion Graph', toggle_btn=False, add_dock_area=True,
             hide_title=False, set_scroll=True)
        for ch in range(GeneralSettings.N_CH):
            self.dock_area.addDock(PortionGraphDock(ch))
