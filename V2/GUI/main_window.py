from PyQt5.QtWidgets import *
# --My Packages--
from V2.GUI.menu_bar import MenuBar
from V2.GUI.toolbar import ToolBar
from V2.GUI.tabs.table_widget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PolyCortex Gui')
        # Tab
        self.table_widget = TableWidget(self)
        self.setCentralWidget(self.table_widget)
        # MenuBar
        self.setMenuBar(MenuBar())
        # Toolbar
        self.init_toolbar()
        # Start Bar
        self.intro_message = 'Running the experiment ...'
        self.statusBar().showMessage(self.intro_message)

    def init_toolbar(self):
        self.addToolBar(ToolBar(self))




