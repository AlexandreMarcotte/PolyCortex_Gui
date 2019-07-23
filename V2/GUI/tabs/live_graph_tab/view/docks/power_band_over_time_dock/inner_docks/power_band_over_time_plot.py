# --General Packages--
import pyqtgraph as pg
# --My Packages--
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget
from V2.utils.waves import waves


class PowerBandOverTimePlot(ScrollPlotWidget):
    def __init__(self, curve_color=('w')):
        super().__init__(curve_color=curve_color)

        self.pos = 0
        self._init_plot_appearance()

    def _init_plot_appearance(self):
        """Create the plot widget and its characteristics"""
        self.plotItem.showGrid(x=True, y=True, alpha=0.3)
        self.plotItem.setLabel(axis='bottom', text='Time', units='Hz')         # TODO: ALEXM : verifier l'uniter
        self.plotItem.setLabel(axis='left', text='Amplitude', units='None')
        self.setXRange(0, 200)

    def connect_signals(self, signals, fft_stage=None):
        super().connect_signals(signals)
        self.fft_stage = fft_stage
        self.curves_points = self._add_curve_point_legend()

    def _update(self):
        for i, signal in enumerate(self.signals):
            self.curves[i].setData(signal)
            self.update_curve_points(i)

    def update_curve_points(self, ch):
        self.pos += 1
        self.curves_points[ch].setPos(self.pos)

    # TODO: ALEXM: Create an object from that
    def _add_curve_point_legend(self):
        curve_points = []
        for i, (curve, wave_name) in enumerate(zip(self.curves, waves)):
            # Curve
            curve_pt = pg.CurvePoint(curve)
            curve_points.append(curve_pt)
            self.addItem(curve_pt)
            # Text
            text = pg.TextItem(wave_name, anchor=(0.5, -1.0))
            text.setParentItem(curve_points[i])
            # Arrow
            arrow = pg.ArrowItem(angle=70)
            arrow.setParentItem(curve_points[i])
        return curve_points
