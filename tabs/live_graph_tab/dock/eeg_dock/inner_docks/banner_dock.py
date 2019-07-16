from tabs.live_graph_tab.dock.inner_dock import InnerDock
from tabs.live_graph_tab.dock.banner_dock.banner import Banner


class BannerDock(InnerDock):
    def __init__(self, main_eeg_dock):
        self.eeg_dock = main_eeg_dock
        super().__init__(
                self.eeg_dock.layout, 'Banner', b_pos=(0, 3), b_checked=False,
                toggle_button=True)
        self.create_dock()

    def create_dock(self):
        # banner_d = InnerDock(
        #     self.eeg_dock.layout, 'Banner', b_pos=(0, 3), b_checked=False,
        #     toggle_button=True, size=(1, 1))
        Banner(self.layout)
        self.eeg_dock.dock_area.addDock(self.dock)
        self.dock.hide()

