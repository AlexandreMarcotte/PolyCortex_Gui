from PyQt5.QtWidgets import *
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea.Dock import DockLabel
import sys
# --My Packages--
from V2.utils.update_style_patch import update_style_patched
from .menu_bar.menu_bar import MenuBar
from .toolbar.toolbar import ToolBar
from .tabs.table_widget import TableWidget
from V2.general_settings import GeneralSettings


class MainWindow(QMainWindow):
    def __init__(self):

        self.app = QApplication(sys.argv)

        super().__init__()
        DockLabel.updateStyle = update_style_patched
        self.setWindowTitle('PolyCortex Gui')
        self.setGeometry(100, 100, 1300, 900)
        # Tab
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        # MenuBar
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        # Toolbar
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)
        # Start Bar
        self.intro_message = 'Running the experiment ...'
        self.statusBar().showMessage(self.intro_message)

    def set_main_window_in_general_settings(self):
        GeneralSettings.main_window = self

    def excec(self):
        QtGui.QApplication.instance().exec_()

