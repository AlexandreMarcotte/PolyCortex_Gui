# -- General Packages --
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import os


class ToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.addAction(ExitAction(self, main_window))


class ExitAction(QAction):
    def __init__(self, tool_bar, main_window):
        self.exit_icon = self.create_exit_icon()
        super().__init__(self.exit_icon, 'Exit', tool_bar)

        self.setShortcut('Ctrl+Q')
        self.setStatusTip('Exit application')
        self.triggered.connect(main_window.close)

    def create_exit_icon(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'GUI/img/exit.png')
        exit_icon = QIcon(path)
        return exit_icon

