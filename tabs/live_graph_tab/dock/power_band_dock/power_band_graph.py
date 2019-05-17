# --General Packages--
import pyqtgraph as pg
# -- My packages --
from ... dock.dock import Dock
from app.pyqt_frequently_used import *


class PowerBandGraph(Dock):
    def __init__(self, gv, layout):
        super().__init__(gv, 'fft', layout)
        self.gv = gv
        self.layout = layout
        # plot_gr, self.plot_layout = create_gr()
        # self.layout.addWidget(plot_gr, 0, 0)
        self.ch = 0

        self.init_choose_ch_combobox()
        self.init_on_off_button()

        self.gv.freq_calculator.set_waves(self.gv.waves)
        self.plot = self.init_plot()
        self.brushes, self.x, self.width = self.init_bar_graph_caract()

        self.N_ELE = len(self.gv.waves)

        self.timer.timeout.connect(self.update)

    def init_plot(self):
        plot = pg.PlotWidget(background=dark_grey)
        self.plot_d.layout.addWidget(plot, 2, 0, 1, 2)
        waves_names = [wave_name for wave_name in self.gv.waves]
        plot.plotItem.setLabel(axis='left', text='Power', units='None')
        plot.plotItem.setLabel(axis='bottom', text=waves_names)
        return plot

    def init_bar_graph_caract(self):
        brushes = [pg.mkBrush(i) for i in range(len(self.gv.waves))]
        x = [w.get_half_pos() for w in self.gv.waves.values()]
        width = [w.get_delta_range() for w in self.gv.waves.values()]

        return brushes, x, width

    def time_func(self):
        # Timer(self.init_bar_braph_caract())
        pass

    # def add_head_img(self):
    #     mne_head = QLabel()
    #     mne_head.setPixmap(QtGui.QPixmap('./img/mne_head.png'))
    #     self.layout.addWidget(mne_head, 2, 0)

    def update(self):
        self.plot.clear()
        bg = pg.BarGraphItem(
                height=self.gv.freq_calculator.freq_per_band_all_ch[self.ch],              # put the function directly here
                # height=partial(self.gv.freq_calculator.get_avg_freq_per_band, 0),
                x=self.x, width=self.width, brushes=self.brushes)
        self.plot.addItem(bg)

