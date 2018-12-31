# -- Genral packages --
from ... static_graph_tab.graphs.graph import Graph
from app.colors import *
# -- My Packages --
import numpy as np


class PortionGraph(Graph):
    def __init__(self):
        super().__init__()

        self.brushes = [red, green, blue, yellow, purple]
        self.data = np.zeros(200)
        self.t = []
        self.classif_region = None
        self.min_borne = -20
        self.max_borne = 160

    def add_all_experimentation_regions(self, ch, exp):
        """
        Add a sliding region over the place on the graph where an
        experiment value as occure (ie there is a value for experiment type
        different than 0
        """
        # Add a colored region on the plot where an event as occured
        for no, val in enumerate(exp):
            val = int(val)
            if val:
                if (val == 1 or val == 2) and (ch == 0 or ch == 1):
                    self.add_region(
                            [no + self.min_borne, no + self.max_borne],
                            brush_color=self.brushes[int(val)],
                            movable=False)
                elif (val == 3 or val == 4) and (ch == 2 or ch == 3):
                    self.add_region(
                            [no + self.min_borne, no + self.max_borne],
                            brush_color=self.brushes[int(val)],
                            movable=False)