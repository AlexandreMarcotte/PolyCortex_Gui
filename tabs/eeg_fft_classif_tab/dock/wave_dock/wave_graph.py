import pyqtgraph as pg
# -- My packages --
from ... dock.dock import Dock
from app.pyqt_frequently_used import *


class WaveGraph(Dock):
    def __init__(self, gv, layout):
        super().__init__(gv, layout, 'fft', 'Start')
        self.gv = gv
        self.layout = layout

        plot_gr, self.plot_layout = create_gr()
        self.layout.addWidget(plot_gr, 0, 0)
        self.init_on_off_button()

        self.waves = {'delta': Wave((0, 4)),
                      'theta': Wave((4, 8)),
                      'alpha': Wave((8, 12)),
                      'beta': Wave((12, 40)),
                      'gamma': Wave((40, 100))
        }
        self.gv.freq_calculator.set_waves(self.waves)
        self.plot = self.init_plot()
        self.brushes, self.x, self.width = self.init_bar_braph_caract()

        self.N_ELE = len(self.waves)

        self.timer.timeout.connect(self.update)

    def init_plot(self):
        """"""
        plot = pg.PlotWidget(background=dark_grey)
        self.plot_layout.addWidget(plot, 1, 0)
        waves_names = [wave_name for wave_name in self.waves]
        plot.plotItem.setLabel(axis='left', text='Power', units='None')
        plot.plotItem.setLabel(axis='bottom', text=waves_names)
        # Add to tab layout
        self.layout.addWidget(plot, 1, 0)

        return plot

    def init_bar_braph_caract(self):
        brushes = [pg.mkBrush(i) for i in range(len(self.waves))]
        x = [w.get_half_pos() for w in self.waves.values()]
        width = [w.get_delta_range() for w in self.waves.values()]

        return brushes, x, width

    def time_func(self):
        # Timer(self.init_bar_braph_caract())
        pass

    def add_head_img(self):
        mne_head = QLabel()
        mne_head.setPixmap(QtGui.QPixmap('./img/mne_head.png'))
        self.layout.addWidget(mne_head, 2, 0)

    def update(self):
        self.plot.clear()
        bg = pg.BarGraphItem(height=self.gv.freq_calculator.freq_per_band,
                             x=self.x, width=self.width, brushes=self.brushes)
        self.plot.addItem(bg)


class Wave:
    def __init__(self, freq_range):
        self.freq_range = freq_range

    def get_half_pos(self):
        return self.freq_range[0] + (self.get_delta_range()) / 2

    def get_delta_range(self):
        return self.freq_range[1] - self.freq_range[0]