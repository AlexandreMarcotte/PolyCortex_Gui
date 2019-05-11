# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
# --My packages--
from tabs.tab_widget import TabWidget
from .tool_bar import ToolBar
from .menu_bar.menu_bar import MenuBar


class MainWindow(QMainWindow):
    def __init__(self, app, gv):
        super().__init__()
        self.app = app
        self.gv = gv
        self.name = 'PolyCortex Gui'
        self.openbci_logo_path = './img/openbci_logo.png'
        self.file_icon_path = './img/file.png'
        self.polycortex_logo_path_alpha_background = \
                './img/polycortex_logo_alpha_background.png'
        self.polycortex_logo_path =  './img/polycortex_logo.png'
        self.sinus_logo_path = './img/sinus.png'
        self.icon = QtGui.QIcon(self.polycortex_logo_path)
        self.pos = (0, 0)
        self.size = (1350, 950)
        self.intro_message = 'Running the experiment ...'

        self.init_mainwindow()
    
    def init_mainwindow(self):
        self.setWindowTitle(self.name)
        self.setWindowIcon(self.icon)
        self.setGeometry(*self.pos, *self.size)
        # Add a menu bar
        self.menu_bar = MenuBar(self, self.gv)
        # Add a toolbar
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)
        # message at the bottom
        self.statusBar().showMessage(self.intro_message)

        self.tab_w = TabWidget(self, self.gv)
        self.setCentralWidget(self.tab_w)

        self.show()


