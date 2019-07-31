# -- General packages --
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import DockArea
# -- My packages --
from .docks.full_graph_dock.full_graph_docks import FullGraphDocks
from .docks.portion_graph_dock.portion_graph_docks import PortionGraphDocks
from .docks.file_selector_dock.file_selector import FileSelectorDock
from .docks.classification_graph_dock.classification_graph_docks import ClassificationGraphDocks
from ..connectors.static_graph_dock_connector import StaticGraphDockConnector


class StaticGraphTabView(QWidget):
    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._controller = controller

        self._init_ui()
        self._connect()

    def _init_ui(self):
        self.layout = QGridLayout(self)
        self._init_file_selector_dock()

        # Init plot dock area
        self._dock_area = DockArea()
        # Set scroll area to the dock
        self._scoll_area = self._create_scroll_area()
        self.layout.addWidget(self._scoll_area, 1, 0, 1, 4)
        self._scoll_area.setWidget(self._dock_area)

        self._init_plots_docks()

    def _init_file_selector_dock(self):
        self.file_selector_dock = FileSelectorDock(self.layout)

    def _init_plots_docks(self):
        # Add plot dock to it
        self._init_classification_graph_docks()
        self._init_portion_graph_docks()
        self._init_full_graph_docks()

    def _init_classification_graph_docks(self):
        self.classification_graph_docks = ClassificationGraphDocks()
        self._dock_area.addDock(
            self.classification_graph_docks)

    def _init_portion_graph_docks(self):
        self.portion_graph_docks = PortionGraphDocks()
        self._dock_area.addDock(
            self.portion_graph_docks, 'right', self.classification_graph_docks)

    def _init_full_graph_docks(self):
        self.full_graph_docks = FullGraphDocks()
        self._dock_area.addDock(
            self.full_graph_docks, 'right', self.portion_graph_docks)

    def _create_scroll_area(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        return scroll_area

    def _connect(self):
        StaticGraphDockConnector(view=self, model=self._model)

    """
        self.init_tab()

    def init_tab(self):
        self.layout = QGridLayout(self)

        file_selector, left_panel, right_panel = self.create_grps()
        splitter = self.create_splitter(left_panel.gr, right_panel.gr)
        scroller = self.create_scroll(splitter)
        self.add_gr_to_main_widget(file_selector.gr, scroller)

        self.setLayout(self.layout)

        self.connect_updates(right_panel, left_panel)

    def create_grps(self):
        right_panel = RightGraphLayout(self.gv)
        left_panel = LeftGraphLayout(self.gv, right_panel)
        file_selector = FileSelector('File selector', self, self.gv,
                                     right_panel, left_panel)
        return file_selector, left_panel, right_panel

    def create_splitter(self, portion_graph_gr, full_graph_gr):
        sp = QSplitter(Qt.Horizontal)
        sp.addWidget(portion_graph_gr)
        sp.addWidget(full_graph_gr)
        return sp

    def create_scroll(self, splitter):
        sc = QScrollArea()
        sc.setWidgetResizable(True)
        sc.setWidget(splitter)
        return sc

    def add_gr_to_main_widget(self, file_selector_gr, scroller):
        self.layout.addWidget(file_selector_gr)
        self.layout.addWidget(scroller)

    def connect_updates(self, right_panel, left_panel):
        updater = Updater(self.gv)
        updater.connect_all(right_panel, left_panel, self.gv)
    """
