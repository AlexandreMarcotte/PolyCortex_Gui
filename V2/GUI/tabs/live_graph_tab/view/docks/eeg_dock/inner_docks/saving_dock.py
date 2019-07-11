# --My Packages--
from V2.utils.data_saver import DataSaver
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock


class SavingDock(InnerDock):
    def __init__(self, external_layout=None):
        super().__init__(
            name='Saving', toggle_btn=True, add_dock_area=False,
            set_scroll=False, external_layout=external_layout)

        self.data_saver = DataSaver(self.inner_layout)
