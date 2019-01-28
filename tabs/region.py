from app.colors import *
import numpy as np


class Regions:
    """Regions to show classification live on one eeg graph"""
    def __init__(self, gv, N_CLASSIF_R_PER_PLOT):
        self.gv = gv
        self.exp_q = self.gv.experiment_queue
        self.region_waiting = list(range(N_CLASSIF_R_PER_PLOT))

        self.list = []
        self.in_use = []
        self.to_delete = []
        self.brushes = [red, blue, green, yellow, purple]
        self.last_n_data_created = 0

    def detect_exp_event(self):
        """Add vertical lines where experiment events happen you should use
           this method at the same time of running an experiment or while
           reading from a file (then add box with text)
          * Currently only done for the ch 0 """
        event_occure_type = self.find_what_type_of_event_occured()
        event_occure_pos = self.find_where_event_occured()
        # Set the position of the regions delimiting events (when an
        # an experiment is playing
        if event_occure_type != []:
            for no, (pos, n_z) in enumerate(zip(
                        event_occure_pos, event_occure_type)):
                brush = self.brushes[int(n_z)]
                self.list[no][1].setBrush(brush)
                self.list[no][1].setRegion([pos, pos+180])

    def find_what_type_of_event_occured(self):
            return np.array(self.exp_q)[
                    np.nonzero(np.array(self.exp_q))[0]]

    def find_where_event_occured(self):
        return np.nonzero(np.array(self.exp_q))[0]

    def classif_event(self):
        if self.event_occured() and self.region_waiting:
            spawn_region = self.region_waiting.pop()
            self.set_brush(spawn_region)
            self.add_region_to_plot(spawn_region)

        delta_data = self.keep_track_of_n_data_created_between_itt()
        self.move_and_remove_regions(delta_data)

    def event_occured(self):
        list_of_possible_events = [0, 1]
        return self.gv.last_classified_type in list_of_possible_events

    def set_brush(self, spawn_region):
        """Select brush type based on event type"""
        brush = self.brushes[self.gv.last_classified_type]
        self.list[spawn_region][1].setBrush(brush)

    def add_region_to_plot(self, spawn_region):
        self.list[spawn_region][1].setRegion(
            [self.gv.DEQUE_LEN - 180, self.gv.DEQUE_LEN])
        self.in_use.append(spawn_region)
        # Reset classification
        self.gv.last_classified_type = None

    def keep_track_of_n_data_created_between_itt(self):
        """keep track of the number of data that was created between call
           to this function so that the regions pos is updated accordingly"""
        delta_data = self.gv.n_data_created - self.last_n_data_created
        self.last_n_data_created = self.gv.n_data_created
        return delta_data

    def move_and_remove_regions(self, delta_data):
        """Move regions that are in use at every itteration"""
        if self.in_use:
            for r_no in self.in_use:
                self.list[r_no][0] -= delta_data
                pos = self.list[r_no][0]
                self.list[r_no][1].setRegion([pos - 180, pos])
                # Remove regions that are out of view
                if self.list[r_no][0] < 0:
                    self.region_waiting.append(r_no)
                    self.list[r_no][1].setRegion(
                            [self.gv.DEQUE_LEN, self.gv.DEQUE_LEN])
                    self.list[r_no][0] = self.gv.DEQUE_LEN
                    self.to_delete.append(r_no)
        # Remove the regions that are out of the view
        if self.to_delete:
            self.in_use = [
                    x for x in self.in_use if x not in self.to_delete]
            self.to_delete = []
