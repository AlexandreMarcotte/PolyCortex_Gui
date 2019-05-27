# -- General Packages --
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import qdarkstyle
import os
# -- My Packages --
from .my_pop_up import MyPopUp


class ToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.addAction(ExitAction(self, main_window))
        self.addAction(DarkModeAction(self, main_window))
        self.addAction(PolycortexInfoAction(self))


class DarkModeAction(QAction):
    def __init__(self, tool_bar, main_window):
        self.main_window = main_window

        base_path = os.getcwd()
        path = os.path.join(base_path, 'img/light_mode.png')
        super().__init__(QIcon(path), 'change light style', tool_bar)

        self.setStatusTip('Change style to qdarkstyle')
        self.triggered.connect(self.change_light_style)

    def change_light_style(self):
        self.main_window.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


class ExitAction(QAction):
    def __init__(self, tool_bar, main_window):
        exit_icon = self.create_exit_icon()
        super().__init__(exit_icon, 'Exit', tool_bar)

        self.setShortcut('Ctrl+Q')
        self.setStatusTip('Exit application')
        self.triggered.connect(main_window.close)

    def create_exit_icon(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'app/exit.png')
        exit_icon = QIcon(path)
        return exit_icon


class PolycortexInfoAction(QAction):
    def __init__(self, tool_bar):
        polycortex_logo_path = './img/polycortex_logo_alpha_background.png'
        icon = QIcon(polycortex_logo_path)
        super().__init__(icon, 'PolyCortex', tool_bar)

        self.setStatusTip('Get information about PolyCortex Society')
        self.triggered.connect(self.show_polycortex_info_page)
        # self.w = None

    def show_polycortex_info_page(self):
        self.polycortex_info_win = MyPopUp()
        self.polycortex_info_win.show()

