import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import pyqtgraph as pg
# --My Packages--
from .live_plot import LivePlot


class SpectogramPlotWidget(pg.GraphicsLayoutWidget, LivePlot):
    def __init__(self, signals=()):
        super().__init__()
        self.signals = signals
        self.ffts = deque(maxlen=250)

        view_box = pg.ViewBox()
        view_box.setAspectLocked()
        self.spectogram_img = pg.ImageItem()
        view_box.addItem(self.spectogram_img)
        view_box.addItem(pg.GridItem())
        self.addItem(view_box)

        self.timer = self.init_timer()
        self.timer.start(100)

    def update(self):
        self.ffts.append(np.array(self.signals[0])[:80])
        spectogram_img_cmap = self.create_cmap(self.ffts)
        self.spectogram_img.setImage(spectogram_img_cmap)

    @staticmethod
    def create_cmap(z):
        cmap = plt.get_cmap('jet')
        min_z = np.min(z)
        max_z = np.max(z)
        cmap = cmap((z - min_z)/(max_z - min_z))
        return cmap
