from app.colors import *
import numpy as np

# self.gv.n_data_created[0]
class Regions:
    """Regions to show classification live on one eeg graph"""
    def __init__(self, gv, n_classif_regions_per_plot):
        self.gv = gv
        self.exp_q = self.gv.experiment_queue
        self.waiting = list(range(n_classif_regions_per_plot))
        self.last_n_data_created = 0

        self.list = []
        self.in_use = []
        self.to_delete = []
        self.brushes = [red, green, blue, yellow, purple]

    def detect_exp_event(self):
        """Add vertical lines where experiment events happen (then add box
         with text) Do all these action in one line so that its not split
          with an other thread  
          * Currently only done for the ch 0 """
        non_zero_type = np.array(self.exp_q)[np.nonzero(np.array(self.exp_q))[0]]
        non_zero_pos = np.nonzero(np.array(self.exp_q))[0]

        # Set the position of the regions delimiting events (when
        # an experiment is playing
        if non_zero_type != []:
            for no, (pos, n_z) in enumerate(zip(non_zero_pos, non_zero_type)):
                brush = self.brushes[int(n_z)]
                self.list[no][1].setBrush(brush)
                self.list[no][1].setRegion([pos, pos+150])

    def classif_event(self):
        """"""
        # Create region if event occure and add it to the list that update
        # Their position. And if there is enough region left
        if self.gv.last_classified_type[0] and self.waiting:
            spawn_region = self.waiting.pop()
            # Select brush type based on event type
            brush = self.brushes[self.gv.last_classified_type[0] - 6]
            self.list[spawn_region][1].setBrush(brush)
            self.list[spawn_region][1].setRegion([self.gv.DEQUE_LEN - 170,
                                                     self.gv.DEQUE_LEN])
            self.in_use.append(spawn_region)
            self.gv.last_classified_type[0] = 0
        # keep track of the number of data that was created between call
        # to this function so that the regions pos is updated accordingly
        delta_data = self.gv.n_data_created[0] - self.last_n_data_created
        self.last_n_data_created = self.gv.n_data_created[0]
        # Move regions that are in use at every itteration
        if self.in_use:
            for r_no in self.in_use:
                self.list[r_no][0] -= delta_data
                pos = self.list[r_no][0]
                self.list[r_no][1].setRegion([pos - 170, pos])
                # Remove region out of view
                if self.list[r_no][0] < 0:
                    self.waiting.append(r_no)
                    self.list[r_no][1].setRegion([self.gv.DEQUE_LEN,
                                                  self.gv.DEQUE_LEN])
                    self.list[r_no][0] = self.gv.DEQUE_LEN
                    self.to_delete.append(r_no)

        # Remove the regions that are out of the view
        if self.to_delete:
            self.in_use = [x for x in self.in_use \
                             if x not in self.to_delete]
            self.to_delete = []