# -- General Packages --
from functools import partial
# -- My Packages --
from .full_graph_dock import FullGraphDock
from ...static_graph_docks import StaticGraphDocks


class FullGraphDocks(StaticGraphDocks):
    def __init__(self):
        super().__init__('Full Graph', size=(2, 1))

        self._init_docks(dock_type=FullGraphDock)

    def connect_sliders(self):
        for dock in self.docks:
            dock.connect_slider()

