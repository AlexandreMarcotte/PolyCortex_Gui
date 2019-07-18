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

        self.plot = self._view.fft_dock.plot_dock.plot

    def connect(self):
        self._connect_plot()

    def _connect_plot(self):
        self.plot.connect_signals(
            signals=self._model.pipeline.fft_stage.output,
            fft_stage=self._model.pipeline.fft_stage)


