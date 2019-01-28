class EegGraph:
    def __init__(self, ch, q, gv, ts, curve, regions):
        """
        Class containing a single EEG graph
        :param ch:
        :param q:
        :param gv:
        :param ts:
        :param curve:
        :param regions: List of regions that are available for this graph
        """
        self.ch = ch
        self.q = q
        self.gv = gv
        self.ts = ts
        self.curve = curve
        self.regions = regions

        self.i = 0

    def update_graph(self):
        self.update_eeg()
        self.i += 1

    def update_eeg(self):
        # Time channel where we don't have to display any q
        if self.ch == 8:
            self.curve.setData(self.ts, self.q)
        else:
            self.curve.setData(self.q)
            # Detect the occurence of events by placing a region around them
            if self.ch in self.gv.ch_to_classify:
                self.regions.detect_exp_event()
                self.regions.classif_event()