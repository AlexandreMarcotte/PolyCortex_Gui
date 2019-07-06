from PyQt5.QtWidgets import *
# --My Packages--
from .menu_bar import MenuBar
from .toolbar import ToolBar
from .tabs.table_widget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PolyCortex Gui')
        self.setGeometry(100, 100, 600, 500)
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



