class StaticGraphUpdate:
    def __init__(self, region, plot):
        self.region = region
        self.plot = plot

    def update_plot_range(self):
        """
        Update the portion plot (top left) range based on the region position
        on the full graph (right)
        """
        minX, maxX = self.region.getRegion()
        self.plot.setXRange(minX, maxX, padding=0)