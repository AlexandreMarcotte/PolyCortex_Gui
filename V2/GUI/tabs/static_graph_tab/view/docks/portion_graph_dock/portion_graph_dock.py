# -- General Packages --
import pyqtgraph as pg
import numpy as np
# -- My Packages --
from V2.GUI.tabs.inner_dock import InnerDock


class PortionGraphDock(InnerDock):
    def __init__(self, ch):
        super().__init__(f'{ch+1}', toggle_btn=False, hide_title=True,
            auto_orientation=True, background_color=(0, 0, 0))

        self.N_DATA_TOT = 100
        self.left_bound = 10
        self.right_bound = 20
        self.plot_width = self.right_bound - self.left_bound

        self.plot, self.curve = self.init_plot(pos=(0, 0))
        # self.region = self._init_region(
        #     self.plot, brush_color=(255, 0, 0, 50))
        region = pg.LinearRegionItem(values=(12, 16), brush=(0, 0, 250, 50))
        self.plot.addItem(region)

        self.event_plot, self.event_curve = self.init_plot(
            pos=(1, 0), data=np.array([np.random.randint(2) for _ in range(100)]))


    def init_plot(
            self, pos=(0, 0), size=(1, 1), data=np.random.random(100)):
        plot = pg.PlotWidget()
        curve = plot.plot(data)
        curve.setPen('g')
        self.inner_layout.addWidget(plot, *pos, *size)
        return plot, curve

    def _init_region(
            self, plot=None, bounds=(12, 16), movable=True,
            brush_color=(0, 0, 250, 50)):
        """ Add a pyqtgraph region on a single event """
        region = pg.LinearRegionItem(movable=movable)
        region.setRegion(bounds)
        # region.start_pos = bounds[0]
        # region.last_pos = bounds[0]
        plot.addItem(region)
        region.setBrush(brush_color)
        return region

    # def update(self, signal, which_curve):
    #     if which_curve == 'portion_curve':
    #        self.portion_curve.setData(signal)
    #     elif which_curve == 'event_curve':
    #         self.event_curve.setData(signal)



