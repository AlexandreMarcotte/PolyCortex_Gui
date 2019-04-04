# -- My packages -- 
from ... static_graph_tab.groups.group import Group
from ... static_graph_tab.graphs.portion_graph import PortionGraph
from ... static_graph_tab.graphs.avg_classif_graph import AvgClassifGraph
from ... static_graph_tab.graphs.classif_graph import ClassifGraph
from app.colors import *
# -- General packages -- 
from PyQt5.QtGui import *


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
        name = 'Avgerage classification graph - Portion graph - Classification graph'
        parent_layout, self.gr = self.create_gr_and_layout(name)

        self.init_graphs(parent_layout, gv)

    def init_graphs(self, parent_layout, gv):                                # TODO: ALEXM: find how redefinintion of functions are done
        for ch in range(gv.N_CH):
            self.layout, gr = self.create_gr_and_layout(
                    name=f'Electrod {ch + 1}', parent_layout=parent_layout, ch=ch)
            self.create_graphs()

    def create_graphs(self):
        self.create_classif_graph()
        self.create_portion_graph()
        self.create_avg_classif_graph()

    def create_classif_graph(self):
        classif_graph = ClassifGraph(self.gv)
        classif_graph.add_plot(
                self.layout, y=2, x=4, h=2, x_range=self.x_range,
                show_grid=True)
        classif_graph.add_region([self.r_left, self.r_left], yellow)
        self.classif_graphs.append(classif_graph)

    def create_portion_graph(self):
        portion_graph = PortionGraph()
        portion_graph.add_plot(
                self.layout, y=0, x=4, h=2, x_range=self.x_range,
                show_grid=True)
        self.add_red_classif_region(portion_graph)

    def add_red_classif_region(self, portion_graph):
        # Put the classification region inside the full graph region
        portion_graph.add_region(
                [self.r_left, self.r_left + self.gv.emg_signal_len], pale_red)
        portion_graph.classif_region = portion_graph.region
        self.portion_graphs.append(portion_graph)

    def create_avg_classif_graph(self):
        avg_classif_graph = AvgClassifGraph()
        avg_classif_graph.add_plot(
                self.layout, x=0, y=0, h=3, w=4, x_range=170)
        avg_classif_graph.add_classif_num_combobox()
        self.add_combo_classif(avg_classif_graph)
        self.avg_classif_graphs.append(avg_classif_graph)

    def add_combo_classif(self, avg_classif_graph):
        self.layout.addWidget(avg_classif_graph.combo_classif, 3, 0, 1, 4)


