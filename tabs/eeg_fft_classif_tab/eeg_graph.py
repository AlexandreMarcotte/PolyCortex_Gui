from collections import deque
import numpy as np
import pyqtgraph as pg
from functools import partial
# My packages
from app.colors import *
            

class EegPlotsCreator:
    def __init__(self, gv, layout, timers, pen_colors):
        self.gv = gv
        self.ts = self.gv.t_queue
        self.layout = layout
        self.timers = timers
        self.pen_colors = pen_colors
        # self.last_classified_type = last_classified_type
        self.plots = []
        self.eeg_graphes = []
        self.zero_q = deque(
            np.zeros(self.gv.DEQUE_LEN), maxlen=self.gv.DEQUE_LEN)
        # Regions
        self.n_classif_regions_per_plot = 2

        self.create_all_eeg_plot()

    def create_all_eeg_plot(self):
        """
        """
        for ch in range(self.gv.N_CH + 1):
            plot, q, rowspan = self.create_plot(ch)
            self.layout.addWidget(plot, ch*4+3, 1, rowspan, 2)
            curve = self.create_curve(plot, ch, q)
            eeg_graph = EegGraph(ch, q, self.ts, curve, self.regions)
            self.eeg_graphes.append(eeg_graph)
            self.timers[ch].timeout.connect(self.eeg_graphes[ch].update_graph)


    def create_plot(self, ch):
        """Create a plot for all eeg signals and the last to keep track of time"""
        plot = pg.PlotWidget(background=(3, 3, 3))
        plot.plotItem.showGrid(x=True, y=True, alpha=0.2)
        plot.plotItem.setLabel(axis='left', units='v')
        # Create the last plot only to keep track of the time (with zeros as q)
        if ch == self.gv.N_CH:
            # Add the label only for the last channel as they all have the same
            plot.plotItem.setLabel(axis='bottom', text='Time', units='s')      # Todo : ALEXM : verifier l'uniter
            rowspan = 1
            q = self.zero_q  # So that we don't see it
        else:
            plot.plotItem.hideAxis('bottom')
            rowspan = 4
            q = self.gv.data_queue[ch]
            
        self.add_classif_regions_to(plot)

        return plot, q, rowspan

    def add_classif_regions_to(self, plot):
        """Create colored region (10) and placed them all at the beginning
           of each plot (will be used to indicated classification of a
           region of the signal or event occured in experiments"""
        self.regions = Regions(self.n_classif_regions_per_plot)
        for i in range(self.n_classif_regions_per_plot):
            self.regions.list.append(pg.LinearRegionItem([0, 0]))
            plot.addItem(self.regions.list[i], ignoreBounds=True)
        return plot

    def create_curve(self, plot, ch, q):
        """Create curves associated with the plots"""
        eeg_curve = plot.plot(self.ts, q)
        eeg_curve.setPen(self.pen_colors[ch])
        return eeg_curve


class EegGraph:
    def __init__(self, ch, q, ts, curve, regions):
        self.ch = ch
        self.q = q
        self.ts = ts
        self.curve = curve
        self.regions = regions

    def update_graph(self):
        self.update_eeg()
        self.update_regions()

    def update_eeg(self):
        # Time channel where we don't have to display any q
        if self.ch == 8:
            self.curve.setData(self.ts, self.q)
        else:
            self.curve.setData(self.q)

    def update_regions(self):
        """Add vertical lines where experiment events happen (then add box
         with text) Do all these action in one line so that its not split
          with an other thread  """
        pass


# self.gv.n_data_created[0]
class Regions:
    """Regions to show classification live on one eeg graph"""
    def __init__(self, n_classif_regions_per_plot):
        self.list = []
        self.waiting = list(range(n_classif_regions_per_plot))
        self.in_use = []
        self.to_delete = []
        self.brushes = [red, green, blue, yellow, purple]

    def detect_exp_event(self):
        """Classification of event occurence in experimentation
        (currently only done for the ch 0)"""
        non_zero_type = np.array(q)[
            np.nonzero(np.array(q))[0]]
        non_zero_pos = np.nonzero(np.array(q))[0]

        # Set the position of the regions delimiting events (when an
        # an experiment is playing
        if non_zero_type != []:
            for no, (pos, n_z_type) in enumerate(zip(non_zero_pos, non_zero_type)):
                brush = self.brushes[int(n_z_type)]
                self.regions[no][1].setBrush(brush)
                self.regions[no][1].setRegion([pos, pos+150])

     # def classif_event(self):
     #    if self.ch == 3:
     #        # Create region if event occure and add it to the list that update
     #        # Their position. And if there is enough region left
     #        if self.last_classified_type[0] and self.r_waiting:
     #            spawn_region = self.r_waiting.pop()
     #            # Select brush type based on event type
     #            brush = self.region_brush[self.last_classified_type[0] - 6]
     #            self.regions[spawn_region][1].setBrush(brush)
     #            self.regions[spawn_region][1].setRegion([self.N_DATA-170,
     #                                                     self.N_DATA])
     #            self.r_in_use.append(spawn_region)
     #            self.last_classified_type[0] = 0
     #        # keep track of the number of data that was created between call
     #        # to this function so that the regions pos is updated accordingly
     #        delta_data = self.gv.n_data_created[0] - self.last_n_data_created
     #        self.last_n_data_created = self.gv.n_data_created[0]
     #        # Move regions that are in use at every itteration
     #        if self.r_in_use:
     #            for r_no in self.r_in_use:
     #                self.regions[r_no][0] -= delta_data
     #                pos = self.regions[r_no][0]
     #                self.regions[r_no][1].setRegion([pos-170, pos])
     #                # Remove region out of view
     #                if self.regions[r_no][0] < 0:
     #                    self.r_waiting.append(r_no)
     #                    self.regions[r_no][1].setRegion([self.N_DATA,
     #                                                     self.N_DATA])
     #                    self.regions[r_no][0] = self.N_DATA
     #                    self.r_to_delete.append(r_no)
     #
     #        # Remove the regions that are out of the view
     #        if self.r_to_delete:
     #            self.r_in_use = [x for x in self.r_in_use \
     #                             if x not in self.r_to_delete]
     #            self.r_to_delete = []