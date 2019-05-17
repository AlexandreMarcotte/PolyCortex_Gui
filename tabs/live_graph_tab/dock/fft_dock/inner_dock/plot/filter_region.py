# --General Packages--
import pyqtgraph as pg
from functools import partial


class FilterRegion:
    def __init__(self, gv, type, color, min_boundary=0, max_boundary=10):
        self.gv = gv
        self.type = type
        self.min_boundary = min_boundary
        self.max_boundary = max_boundary

        self.region = self.init_region(color)
        self._connect_filter_region()

    def init_region(self, color):
        region = pg.LinearRegionItem(
                values=[self.min_boundary, self.max_boundary],
                brush=color)
        return region

    def _connect_filter_region(self):
        self.region.sigRegionChanged.connect(
                partial(self._update_region_pos))

    def _update_region_pos(self, ):
        self.min_boundary, self.max_boundary  = self.region.getRegion()
        if self.type == 'pass':
            self.gv.min_pass_filter = self.min_boundary
            self.gv.max_pass_filter = self.max_boundary
        elif self.type == 'cut':
            self.gv.min_cut_filter = self.min_boundary
            self.gv.max_cut_filter = self.max_boundary