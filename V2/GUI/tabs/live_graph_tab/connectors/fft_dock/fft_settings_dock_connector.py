## cannot import because of cyclical recursive import :
# https://stackoverflow.com/questions/41250081/python-recursive-import-issue
# from V2.GUI.tabs.live_graph_tab.view.view import View
from functools import partial


class FftSettingsDockConnector:
    def __init__(self, n_ch, view): #: View):   # if you want to see the relative import
        self._n_ch = n_ch
        self._view = view

        self.plot = self._view.fft_dock.plot_dock.plot
        self.settings_dock = self._view.fft_dock.settings_dock
        self.spectrogram_dock = self._view.spectrogram_dock
        self.spectrogram_3d_dock = self._view.spectrogram_3d_dock
        self.power_band_dock = self._view.power_band_dock
        self.power_band_over_time_dock = self._view.power_band_over_time_dock

    def connect(self):
        self._connect_axis(cb=self.settings_dock.scale_freq_axis_cb, axis='x')
        self._connect_axis(cb=self.settings_dock.max_microV_cb, axis='y')
        self._connect_log_axis()
        self._connect_start_btn()

    def _connect_axis(self, cb, axis='x'):
        # Connect function
        scale_axis = self.plot.scale_axis
        cb.activated[str].connect(partial(scale_axis, axis=axis))

    def _connect_log_axis(self):
        self.settings_dock.log_cb.activated[str].connect(self.plot.set_log_mode)

    def _connect_start_btn(self):
        # FFT dock
        self.settings_dock.start_btn.clicked.connect(
            partial(self.plot.connect_timers, t_interval=200))
        # Power band over time
        self.power_band_over_time_dock.settings_dock.start_btn.clicked.connect(
            partial(self.power_band_over_time_dock.plot.plot.connect_timers,
                    t_interval=200))

        # Spectrogram
        self.spectrogram_dock.settings_dock.start_btn.clicked.connect(
            self.spectrogram_dock.plot.start_timer)
        # Spectrogram 3D
        self.spectrogram_3d_dock.settings_dock.start_btn.clicked.connect(
            self.spectrogram_3d_dock.plot.start_timer)
        # Power band
        self.power_band_dock.settings_dock.start_btn.clicked.connect(
            self.power_band_dock.plot.start_timer)

