# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock


class MainDock(InnerDock):
    def __init__(self, name='', settings_dock=None, plot_dock=None,
                 margin=(0, 0, 0, 0)):
        super().__init__(
            name=name, toggle_btn=False, add_dock_area=True,
            set_scroll=True, hide_title=False, margin=margin)

        self.settings_dock = settings_dock(self.inner_layout)
        self.plot_dock = plot_dock

        self.inner_docks = [self.settings_dock, self.plot_dock]
        self._add_all_dock_to_dock_area()

    def _add_all_dock_to_dock_area(self):
        for inner_dock in self.inner_docks:
            self.dock_area.addDock(inner_dock)

    def add_dock(self, dock, relative_pos, other_dock):
        self.dock_area.addDock(dock, relative_pos, other_dock)

