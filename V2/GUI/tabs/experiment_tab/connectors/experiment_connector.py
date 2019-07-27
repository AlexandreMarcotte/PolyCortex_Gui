from V2.GUI.tabs.experiment_tab.docks.emg_experiment.emg_dock import EmgDock
# from V2.GUI.tabs.experiment_tab.experiment_tab_view import ExperimentTabView
# from V2.GUI.tabs.model.model import Model

class ExperimentConnector:
    # def __init__(self, view: ExperimentTabView, model: Model):
    def __init__(self, view, model):

        self._view = view
        self._model = model

        self._connect_emg_experiment()

    def _connect_emg_experiment(self):
        self._view.binary_exp_dock.connect_signal_collector(
            self._model.pipeline.signal_collector)


