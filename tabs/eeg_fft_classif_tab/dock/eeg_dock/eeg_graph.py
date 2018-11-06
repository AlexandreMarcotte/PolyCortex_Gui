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