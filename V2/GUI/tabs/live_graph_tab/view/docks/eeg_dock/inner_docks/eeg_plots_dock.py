from typing import List
# --My packages--
from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from .eeg_plot_dock import EegPlotDock
from .time_plot import TimePlot
from V2.GUI.tabs.live_graph_tab.plot_dock import PlotDock
from V2.utils.colors import Color
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


class EegPlotsDock(InnerDock):
    def __init__(self, size=(1, 10), N_CH=8):
        super().__init__(
            name='eeg_plots_dock', size=size, toggle_btn=False,
            add_dock_area=True, set_scroll=True)

        self._N_CH = N_CH

        self._init_plots()

    def _init_plots(self):
        self._init_eeg_plots()
        self._init_time_plot()

    def _init_eeg_plots(self):
        self.plot_dock_list: List[EegPlotDock] = []
        for ch in range(self._N_CH):
            curve_color = (Color.pen_colors[ch])

            plot_dock = EegPlotDock(
                ch, plot=ScrollPlotWidget(curve_color),
                curve_color=curve_color)

            self.plot_dock_list.append(plot_dock)
            self.dock_area.addDock(plot_dock)

    def _init_time_plot(self):
        self.time_dock = PlotDock(plot=TimePlot(curve_color=('k')))
        self.dock_area.addDock(self.time_dock)

    def hide_pins_settings(self, checked):
        if checked:
            for plot_dock in self.plot_dock_list:
                plot_dock.pins_settings.hide_pins_settings()
        else:
            for plot_dock in self.plot_dock_list:
                plot_dock.pins_settings.show_pins_settings()
