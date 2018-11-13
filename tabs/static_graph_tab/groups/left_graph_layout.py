from ... static_graph_tab.groups.group import Group
from ... static_graph_tab.graphs.portion_graph import PortionGraph
from ... static_graph_tab.graphs.avg_classif_graph import AvgClassifGraph
from ... static_graph_tab.graphs.classif_graph import ClassifGraph

from app.colors import *

class LeftGraphLayout(Group):
    def __init__(self, gv, right_panel):
        super().__init__()
        self.gv = gv
        right_panel = right_panel
        self.r_left = right_panel.full_graphs[0].region.boundingRect().left()

        self.portion_graphs = []
        self.classif_graphs = []
        self.avg_classif_graphs = []

        self.x_range = 2000
        name = 'Avg classif graph - Portion graph - Classif graph'
        parent_layout, self.gr = self.create_gr_and_layout(name)
        self.add_all_graph(parent_layout, gv)

    def add_all_graph(self, parent_layout, gv):                                # TODO: ALEXM: find how redefinintion of functions are done
        for ch in range(gv.N_CH):
            layout, gr = self.create_gr_and_layout(
                name=f'ch {ch + 1}', parent_layout=parent_layout, ch=ch)
            self.create_graphs(layout)

    def create_graphs(self, layout):
        self.create_portion_graph(layout)
        self.create_classif_graph(layout)

    def create_classif_graph(self, layout):
        avg_classif_graph = AvgClassifGraph()
        avg_classif_graph.add_plot(layout, h=2, w=4, x_range=170)
        self.avg_classif_graphs.append(avg_classif_graph)
        classif_graph = ClassifGraph(self.gv)
        classif_graph.add_plot(
            layout, y=1, x=4, x_range=self.x_range, show_grid=True)
        classif_graph.add_region([self.r_left, self.r_left], yellow)
        self.classif_graphs.append(classif_graph)

    def create_portion_graph(self, layout):
        portion_graph = PortionGraph()
        portion_graph.add_plot(layout, y=0, x=4, x_range=self.x_range)
        self.add_red_classif_region(portion_graph)
        
    def add_red_classif_region(self, portion_graph):
        # Put the classification region inside the full graph region
        portion_graph.add_region(
            [self.r_left, self.r_left + self.gv.emg_signal_len], pale_red)
        portion_graph.classif_region = portion_graph.region
        self.portion_graphs.append(portion_graph)
