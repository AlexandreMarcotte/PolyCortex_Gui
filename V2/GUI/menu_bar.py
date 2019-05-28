from PyQt5.QtWidgets import *


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.control_panel_menu = ControlPanelMenu()
        self.addMenu(self.control_panel_menu)


class ControlPanelMenu(QMenu):
    def __init__(self):
        super().__init__('System Control Panel')
        self.stream_from_file = StreamFromFileAction('From Synthetic data')
        self.addAction(self.stream_from_file)


class StreamFromFileAction(QAction):
    pass
