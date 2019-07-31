# -- General Packages --
from functools import partial
# -- My Packages --
from V2.GUI.tabs.model.model import Model


class StaticGraphDockConnector:
    # from V2.GUI.tabs.static_graph_tab.view.static_graph_tab_view import StaticGraphTabView
    # def __init__(self, view: StaticGraphTabView, model: Model):
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._connect()

    def _connect(self):
        self._connect_open_file_btn()
        self._connect_full_graph_slider()

    def _connect_open_file_btn(self):
        self._view.file_selector_dock.open_file_btn.clicked.connect(
            partial(self._connect_signals))

    def _connect_signals(self):
        signals = self._model.load_data()
        self._view.full_graph_docks.update_signals(signals)
        self._view.portion_graph_docks.update_signals(signals)

    def _connect_full_graph_slider(self):
        self._view.full_graph_docks.connect_sliders()

