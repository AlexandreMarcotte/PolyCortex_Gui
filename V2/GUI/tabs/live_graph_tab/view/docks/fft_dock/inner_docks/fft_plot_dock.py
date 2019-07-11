# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
import pyqtgraph.opengl as gl


class FftPlotsDock(InnerDock):
    def __init__(self, size=(1, 10)):
        super().__init__(
                name='fft_plots_dock', size=size, toggle_btn=False,
                add_dock_area=True, set_scroll=True)
        self.view = self._init_plot()

    def _init_plot(self):
        """     """
        view = gl.GLViewWidget()
        view.opts['distance'] = 370
        view.opts['azimuth'] = 40
        view.opts['elevation'] = 15
        return view

