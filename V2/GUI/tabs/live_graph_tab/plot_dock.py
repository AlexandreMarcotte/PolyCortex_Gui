from pyqtgraph.dockarea import *
# --My packages--
from pyqtgraph.dockarea.Dock import DockLabel
from V2.utils.update_style_patch import update_style_patched
from V2.utils.action_btn import Btn
from V2.utils.lable_btn import LabelBtn
from V2.utils.colors import *
from V2.GUI.tabs.live_graph_tab.view.plot_widgets.scroll_plot_widget import ScrollPlotWidget


class PlotDock(Dock):
    def __init__(self, ch, add_btn=True):
        self._ch = ch

        DockLabel.updateStyle = update_style_patched
        super().__init__(str(ch), hideTitle=True)

        self._add_plot()
        if add_btn:
            self._add_all_btn()

    def _add_plot(self):
        self.scroll_plot = ScrollPlotWidget()
        self.addWidget(self.scroll_plot, 0, 1, 3, 9)

    def _add_all_btn(self):
        # Just for visualisation test at the moment
        self.toggle_btn = self._add_toggle_on_off_btn()
        self._add_action_btn()

    def _add_toggle_on_off_btn(self):
        toggle_btn = Btn(
                name=str(self._ch+1), max_width=19, max_height=19,
                color=button_colors[self._ch], toggle=True,
                tip=f'Start/Stop the ch{self._ch+1} signal')

        self.addWidget(toggle_btn, 0, 0, 1, 1)
        return toggle_btn

    def _add_action_btn(self):
        # Average btn
        self.avg_value_btn = LabelBtn(
            name='A', tip='Show average value of queue', conn_func='avg')
        # Maximum btn
        self.max_value_btn = LabelBtn(
            name='M', tip='Show maximum value of queue', conn_func='max')
        #  btn
        self.fft_size_btn = LabelBtn(
            name='F', tip='''Show the size of the fft window on 
            which the fft is calculated for all ch''')

        for no, btn in enumerate(
                [self.avg_value_btn, self.max_value_btn, self.fft_size_btn]):
            self.addWidget(btn, no, 10, 1, 1)
            self.addWidget(btn.label, no, 9, 1, 1)

