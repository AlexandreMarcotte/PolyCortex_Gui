from V2.GUI.tabs.inner_dock import InnerDock
from V2.general_settings import GeneralSettings
from .classification_graph_dock import ClassificationGraphDock


class ClassificationGraphDocks(InnerDock):
    def __init__(self):
        super().__init__(
            'Classification graph', toggle_btn=False, add_dock_area=True,
            hide_title=False)
        for ch in range(GeneralSettings.N_CH):
            self.dock_area.addDock(ClassificationGraphDock(ch))
