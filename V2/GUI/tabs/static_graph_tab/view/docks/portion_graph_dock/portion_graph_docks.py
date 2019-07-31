from .portion_graph_dock import PortionGraphDock
from ...static_graph_docks import StaticGraphDocks


class PortionGraphDocks(StaticGraphDocks):
    def __init__(self):
        super().__init__('Portion Graph', size=(2, 1))

        self._init_docks(dock_type=PortionGraphDock)

