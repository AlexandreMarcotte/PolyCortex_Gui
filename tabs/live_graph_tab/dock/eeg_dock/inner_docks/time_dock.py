from tabs.live_graph_tab.dock.inner_dock import InnerDock


class TimeDock:
    def __init__(self, eeg_dock):
        self.eeg_dock = eeg_dock
        self.create_time_dock()

    def create_time_dock(self):
        self.time_d = InnerDock(self.eeg_dock.layout, 'time dock', size=(1, 1))
        self.eeg_dock.add_ch_layout(
            self.time_d.layout, ch=self.eeg_dock.gv.N_CH, time_ch=True,
            plot_pos=(0, 0))
        self.eeg_dock.dock_area.addDock(self.time_d.dock)

