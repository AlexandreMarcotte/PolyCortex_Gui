import numpy as np
from pyqtgraph.Qt import QtGui
from PyQt5 import QtCore
import pyqtgraph as pg
from pyqtgraph.dockarea import Dock
# -- My packages --
from V2.utils.create_map import create_cmap
from V2.utils.waves import waves
from V2.pipeline.pipeline_stages.fft_stage.fft_stage import FftStage


class SpectrogramPlot(Dock):
    def __init__(self):
        super().__init__(name='', hideTitle=True)

        self.ch = 0
        pg_layout, self.img = self.init_img_view_box()
        self.addWidget(pg_layout)

        self._connect_timer()

    def connect_signal(self, fft_stage: FftStage):
        self.fft_stage = fft_stage
        self.fft_over_time = self.fft_stage.fft_over_time

    def _connect_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

    def start_timer(self):
        self.timer.start(20)

    def init_img_view_box(self):
        """"""
        vb = pg.ViewBox()
        vb.setAspectLocked()

        self.add_axis_name(
            vb, name='Time (n of freq calculated)', pos=(100, 0), angle=0)
        self.add_axis_name(
            vb, name='Frequency (Hz - need to correct)', pos=(-10, 50),
            angle=90)

        # img of the spectrogram_dock
        img = pg.ImageItem(border='w')                                                   # TODO: ALEXM: rotate so that it is in the right direction (longest with longest)
        vb.addItem(img)
        # grid
        g = pg.GridItem()
        vb.addItem(g)
        # wave name txt
        self.add_wave_name_txt_label(vb)

        pg_layout = pg.GraphicsLayoutWidget()
        pg_layout.addItem(vb)
        return pg_layout, img

    def add_axis_name(self, vb, name, pos=(0, 0), angle=0):
        font = QtGui.QFont()
        font.setPixelSize(10)
        axis = pg.TextItem(name, angle=angle)
        axis.setFont(font)
        axis.setPos(*pos)
        vb.addItem(axis)

    def add_axis(self, vb, orientation, height, label):
        axis = pg.AxisItem(orientation=orientation, showValues=False)
        axis.setHeight(height)
        axis.setLabel(label)
        vb.addItem(axis)

    def add_wave_name_txt_label(self, vb):
        # pen for lines
        pen = pg.mkPen(color=(255, 255, 255, 90), width=1)
        # brain wave freq text
        for w_name, w in waves.items():
            w_freq_begin_pos = w.freq_range[0]
            # (vertical line) - Separation line between the different wave frequencies
            l = pg.InfiniteLine(w_freq_begin_pos, angle=0, pen=pen)
            vb.addItem(l)

            # (txt) - Add the name of each specific wave frequency
            if w_name == 'gamma':
                w_freq_end_pos = w.freq_range[1]
                l = pg.InfiniteLine(w_freq_end_pos, angle=0, pen=pen)
                vb.addItem(l)

            font = QtGui.QFont()
            font.setPixelSize(10)
            w_name_item = pg.TextItem(w_name, anchor=(1, 1))
            w_name_item.setFont(font)
            w_name_item.setPos(0, w_freq_begin_pos)
            vb.addItem(w_name_item)
            vb.setXRange(-10, 200)
            vb.setYRange(-10, 110)

    def update(self):
        fft_over_t = np.array(self.fft_over_time[self.ch])
        fft_over_t = np.flip(fft_over_t, 0)  # Or should I rotate the image instead
        cmap = create_cmap(fft_over_t)  # The creation of cmap create quite
        # a lot more lag then the old version without it
        self.img.setImage(cmap)
        # TODO: ALEXM: change the size of the img to have the right frequency
