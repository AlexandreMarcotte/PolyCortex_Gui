from PyQt5.QtWidgets import *
from .control_panel_menu import ControlPanelMenu


class MenuBar(QMenuBar):
    def __init__(self, main_window):
        super().__init__()
        self.control_panel_menu = ControlPanelMenu(main_window)
        self.addMenu(self.control_panel_menu)




