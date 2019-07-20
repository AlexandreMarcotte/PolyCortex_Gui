# --General Packages--
from pyqtgraph import LinearRegionItem
from functools import partial
# --My Packages--
from V2.utils.colors import Color


class FilterRegion(LinearRegionItem):
    def __init__(self, min_boundary=0, max_boundary=10, color=Color.blue):
        super().__init__(values=[min_boundary, max_boundary], brush=color)
        self.color = color
        self.min_boundary = min_boundary
        self.max_boundary = max_boundary

        self.sigRegionChanged.connect(self._update_region_boundaries)

    def _update_region_boundaries(self):
        self.min_boundary, self.max_boundary = self.getRegion()
        # print(self.color, 'min', self.min_boundary, 'max', self.max_boundary)

    # def connect_filter_region(self, sig_filter):
    #     """Connect the filter region to the filter inside the connector module"""
    #     self.sig_filter = sig_filter
    #     self.sigRegionChanged.connect(
    #             partial(self._update_region_pos))

    # def _update_region_pos(self, ):
    #     self.min_boundary, self.max_boundary = self.region.getRegion()
    #     self.sig_filter.min_boundary = self.min_boundary
    #     self.sig_filter.max_boundary = self.max_boundary
#
