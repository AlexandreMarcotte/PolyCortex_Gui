# -*- coding: utf-8 -*-
# -- General packages --
from pyqtgraph.dockarea import *
# -- My packages --
from tabs.live_graph_tab.dock.inner_dock import InnerDock
from tabs.live_graph_tab.dock.fft_dock.inner_dock.settings.settings_inner_dock import SettingsInnerDock
from tabs.live_graph_tab.dock.fft_dock.inner_dock.plot.plot_inner_dock import PlotInnerDock


class FftDock:
    def __init__(self, gv, layout):
        self.gv = gv
        self.layout = layout

        self.dock_area = DockArea()
        layout.addWidget(self.dock_area, 1, 0, 1, 8)

        # Inner plot dock
        self.plot_inner_dock = PlotInnerDock(self.gv, self.layout)
        self.dock_area.addDock(self.plot_inner_dock.dock)

        # Inner settings dock
        self.settings_inner_dock = SettingsInnerDock(
                self.gv, self, self.plot_inner_dock)
        self.dock_area.addDock(self.settings_inner_dock.dock, 'top')

        # Filter settings
        self.filter_inner_dock = self._init_filter_inner_dock()

    def _init_filter_inner_dock(self):
        inner_dock = InnerDock(
                self.layout, 'Filter', toggle_button=True, size=(1, 1),
                b_pos=(0, 1), b_checked=False)
        self.dock_area.addDock(inner_dock.dock, 'right')
        inner_dock.dock.hide()
        return inner_dock

