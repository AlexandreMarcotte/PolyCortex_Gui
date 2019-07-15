# --My packages--
from V2.GUI.tabs.live_graph_tab.model.model import Model
from V2.GUI.tabs.live_graph_tab.view.view import View
from .controller import Controller


class LiveGraphTab:
    def __init__(self):

        self._model = Model()
        self.controller = Controller(self._model)
        self._view = View(self._model, self.controller)


