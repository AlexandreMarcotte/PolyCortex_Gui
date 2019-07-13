class FftPlotsDockConnector:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self.plot_dock = self._view.fft_dock.plot_dock

    def connect(self):
        self.connect_plot()

    def connect_plot(self):
        signals = [self._model.pipeline.fft_stage.output[ch] for ch in range(8)]
        self.plot_dock.plot.connect_signals(signals)
        self.plot_dock.plot.connect_timers()
