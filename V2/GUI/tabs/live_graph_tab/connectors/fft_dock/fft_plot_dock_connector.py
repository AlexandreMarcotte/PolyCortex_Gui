# --General Packages--
from functools import partial
# --My Packages--
# from V2.GUI.tabs.live_graph_tab.view.view import View
# from V2.GUI.tabs.live_graph_tab.model.model import Model


class FftPlotsDockConnector:
    # def __init__(self, view: View, model: Model):
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self.fft_plot = self._view.fft_dock.plot_dock.plot
        self.spectrogram_plot = self._view.spectrogram_dock.plot
        self.spectrogram_3d_plot = self._view.spectrogram_3d_dock.plot
        self.power_band_plot = self._view.power_band_dock.plot
        self.power_band_over_time_plot = self._view.power_band_over_time_dock.plot

    def connect(self):
        self._connect_fft_plot()
        self._create_filter_regions_from_pipeline_filter_stages()
        self._connect_spectrogram_plot()
        self._connect_spectrogram_3d_plot()
        self._connect_power_band_plot()
        self._connect_power_band_over_time_plot()

    def _connect_fft_plot(self):
        self.fft_plot.connect_signals(
            signals=self._model.pipeline.fft_stage.output,
            fft_stage=self._model.pipeline.fft_stage)

    def _connect_filters(self):
        # self.sigRegionChanged.connect(self._update_region_boundaries)
        # TODO: ALEXM: Use a dictionnary for the filters
        # Connect band cut filter
        # bc = self.fft_plot.filters['bandstop'][0]
        # self._connect_filter(bc, 'bandstop')
        # Connect band pass filter
        # bp = self.fft_plot.filters['bandpass'][0]
        # self._connect_filter(bp, 'bandpass')
        pass

    def _create_filter_regions_from_pipeline_filter_stages(self):
        for filter_list in self._model.pipeline.filter_stage.filters.values():
            for filter in filter_list:
                # Create filters
                filter_region = self.fft_plot.create_filter_from_filter_stage(filter)
                # Connect filter
                self._connect_filter(filter_region, filter)

    def _connect_filter(self, filter_region, filter):
        filter_region.sigRegionChanged.connect(partial(
            filter.set_filter_coeff_from_filter_region,
            filter_region=filter_region))

    def _connect_power_band_over_time_plot(self):
        self.power_band_over_time_plot.plot.connect_signals(
            signals=self._model.pipeline.fft_stage.all_freq_band_over_time[0].wave_type_data,
            fft_stage=self._model.pipeline.fft_stage)

    def _connect_spectrogram_plot(self):
        self.spectrogram_plot.connect_signal(
            fft_stage=self._model.pipeline.fft_stage)

    def _connect_spectrogram_3d_plot(self):
        self.spectrogram_3d_plot.connect_signal(
            fft_stage=self._model.pipeline.fft_stage)

    def _connect_power_band_plot(self):
        self.power_band_plot.connect_signal(
            fft_stage=self._model.pipeline.fft_stage)

