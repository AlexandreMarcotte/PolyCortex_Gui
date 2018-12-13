import numpy as np
# -- My packages --
from ... dock.dock import Dock
import pyqtgraph.opengl as gl
from app.pyqt_frequently_used import *
from app.activation_b import btn
import pyqtgraph as pg


class FftOverTimeGraph2D(Dock):
    def __init__(self, gv, layout):

        super().__init__(gv, 'fft', layout)
        self.gv = gv
        self.layout = layout

        self.ch = 0

        pg_layout, self.img = self.init_img_view_box()

        self.secondary_layout.addWidget(pg_layout, 3, 0, 1, 2)

        self.init_choose_ch_combobox()
        self.init_on_off_button()

        self.timer.timeout.connect(self.update)

    def init_img_view_box(self):
        """"""
        vb = pg.ViewBox()
        vb.setAspectLocked()
        img = pg.ImageItem()
        vb.addItem(img)
        pg_layout = pg.GraphicsLayoutWidget()
        pg_layout.addItem(vb)
        return pg_layout, img

    def update(self):
        fft_over_t = np.array(self.gv.freq_calculator.fft_over_time[self.ch])
        self.img.setImage(fft_over_t)


