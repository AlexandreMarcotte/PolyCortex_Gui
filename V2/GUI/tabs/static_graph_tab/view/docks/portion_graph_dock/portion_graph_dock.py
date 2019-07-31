# -- General Packages --
from PyQt5.QtWidgets import QComboBox
# -- My Packages --
from V2.GUI.tabs.static_graph_tab.view.static_graph_dock import StaticGraphDock


class PortionGraphDock(StaticGraphDock):
    def __init__(self, ch):
        super().__init__(ch)

        self.plot, self.curve = self.init_plot(pos=(0, 0))
        self.region = self._init_region(
            self.plot, brush_color=(255, 0, 0, 50))

        self.event_plot, self.event_curve = self.init_plot(pos=(1, 0))


    # def update(self, signal, which_curve):
    #     if which_curve == 'portion_curve':
    #        self.portion_curve.setData(signal)
    #     elif which_curve == 'event_curve':
    #         self.event_curve.setData(signal)



