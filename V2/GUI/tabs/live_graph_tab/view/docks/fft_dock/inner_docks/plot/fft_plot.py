from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


class FftPlot(ScrollPlotWidget):
    def __init__(self, curve_color=('w')):
        super().__init__(curve_color=curve_color)

    def _init_plot_appearance(self):
        self.setYRange(0, 2000000)
        self.setXRange(0, 500)
        self.plotItem.setLabel(axis='left', text='Amplitude')
        self.plotItem.setLabel(axis='bottom', text='Frequency')
