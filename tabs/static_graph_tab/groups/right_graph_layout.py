# -- My packages --
from PyQt5.QtWidgets import *
from .group import Group
from ... static_graph_tab.graphs.full_graph import FullGraph


class RightGraphLayout(Group):
    def __init__(self, gv):
        super().__init__()

        self.full_graphs = []
        self.sliders = []

        parent_layout, self.gr = self.create_gr_and_layout(
                'Full graph')
        self.add_all_graph(parent_layout, gv)

    def add_all_graph(self, parent_layout, gv):                                # TODO: ALEXM: find how redefinintion of functions are done
        for ch in range(gv.N_CH):
            layout, gr = self.create_gr_and_layout(
                name=f'', parent_layout=parent_layout, ch=ch)
            self.create_graphs(layout)

    def create_graphs(self, layout):
        full_graph = FullGraph()
        full_graph.add_plot(layout, show_grid=True, alpha=0.3)
        full_graph.add_region(bounds=[0, 1500])
        slider = full_graph.add_slider(layout, 10000)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1000)
        self.sliders.append(slider)
        self.full_graphs.append(full_graph)
