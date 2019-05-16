from pyqtgraph.dockarea import *


class N100Dock:
    def __init__(self, area, below_dock):
        self.init_dock(area, below_dock)

    def init_dock(self, area, below_dock):
        dock = Dock('N100 experiment')
        area.addDock(dock, 'above', below_dock)