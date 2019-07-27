# -- General packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyqtgraph.dockarea import DockArea
# -- My packages --
from .docks.full_graph_dock.full_graph_docks import FullGraphDocks
from .docks.portion_graph_dock.portion_graph_docks import PortionGraphDocks
from .docks.file_selector_dock.file_selector import FileSelectorDock


class StaticGraphTabView(QWidget):
    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._controller = controller

        self._init_ui()

    def _init_ui(self):
        self.area = DockArea()
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.area)
        self._init_docks()

    def _init_docks(self):
        self._init_file_selector_dock()
        self._init_full_graph_docks()
        self._init_portion_graph_docks()

    def _init_full_graph_docks(self):
        self._full_graph_docks = FullGraphDocks()
        self.area.addDock(self._full_graph_docks)

    def _init_portion_graph_docks(self):
        self._portion_graph_docks = PortionGraphDocks()
        self.area.addDock(
            self._portion_graph_docks, 'left', self._full_graph_docks)

    def _init_file_selector_dock(self):
        self._file_selector_dock = FileSelectorDock(external_layout=self.layout)
        self.area.addDock(self._file_selector_dock)
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
