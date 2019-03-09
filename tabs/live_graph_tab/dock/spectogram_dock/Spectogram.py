import numpy as np
from pyqtgraph.Qt import QtGui
# -- My packages --
from ... dock.dock import Dock
import pyqtgraph as pg
from app.pyqt_frequently_used import create_cmap

class Spectogram(Dock):
    def __init__(self, gv, layout):

        super().__init__(gv, 'fft', layout)
        self.gv = gv
        self.layout = layout

        self.ch = 0

        pg_layout, self.img = self.init_img_view_box()

        self.plot_d.layout.addWidget(pg_layout, 3, 0, 1, 2)

        self.init_choose_ch_combobox()
        self.init_on_off_button()

        self.timer.timeout.connect(self.update)

    def init_img_view_box(self):
        """"""
        vb = pg.ViewBox()
        vb.setAspectLocked()
        # Add axis
        # self.add_axis(vb, 'left', 200, '')
        # self.add_axis(vb, 'bottom', 0, 'T')
        # self.add_axis_name(vb)
        self.add_axis_name(
                vb, name='Time (n of freq calculated)', pos=(100, 0), angle=0)
        self.add_axis_name(
            vb, name='Frequency (Hz - need to correct)', pos=(-10, 50),
            angle=90)

        # img of the spectrogram
        img = pg.ImageItem()                                                   # TODO: ALEXM: rotate so that it is in the right direction (longest with longest)
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
        for w_name, w in self.gv.waves.items():
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
        fft_over_t = np.array(self.gv.freq_calculator.fft_over_time[self.ch])
        fft_over_t = np.flip(fft_over_t, 0)  # Or should I rotate the image instead
        cmap = create_cmap(fft_over_t)  # The creation of cmap create quite
        # a lot more lag then the old version without it
        self.img.setImage(cmap)



