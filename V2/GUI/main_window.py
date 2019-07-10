from PyQt5.QtWidgets import *
from pyqtgraph.Qt import QtGui
from pyqtgraph.dockarea.Dock import DockLabel
import sys
# --My Packages--
from V2.utils.update_style_patch import update_style_patched
from .menu_bar import MenuBar
from .toolbar.toolbar import ToolBar
from .tabs.table_widget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self):

        self.app = QApplication(sys.argv)

        super().__init__()
        DockLabel.updateStyle = update_style_patched
        self.setWindowTitle('PolyCortex Gui')
        self.setGeometry(100, 100, 1200, 800)
        # Tab
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        # MenuBar
        self.setMenuBar(MenuBar())
        # Toolbar
        self.addToolBar(ToolBar(self))
        # Start Bar
        self.intro_message = 'Running the experiment ...'
        self.statusBar().showMessage(self.intro_message)

    def excec(self):
        QtGui.QApplication.instance().exec_()

