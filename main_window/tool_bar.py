# -- General Packages --
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon
import qdarkstyle
import os
# -- My Packages --
from .my_pop_up import MyPopUp


class ToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.polycortex_logo_path_alpha_background = \
            './img/polycortex_logo_alpha_background.png'

        self.create_toolbar()

    def create_toolbar(self):
        self.addAction(self.create_exit_action())
        self.addAction(self.create_dark_mode_activator())
        self.addAction(self.create_polycortex_info_btn())

    def create_exit_action(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'app/exit.png')
        exitIcon = QIcon(path)
        exit_actn = QAction(exitIcon, 'Exit', self.main_window)
        exit_actn.setShortcut('Ctrl+Q')
        exit_actn.setStatusTip('Exit application')
        exit_actn.triggered.connect(self.main_window.close)
        return exit_actn

    def create_dark_mode_activator(self):
        base_path = os.getcwd()
        path = os.path.join(base_path, 'img/light_mode.png')
        light_act = QAction(QIcon(path), 'change light style', self.main_window)
        light_act.setStatusTip('Change style to qdarkstyle')
        light_act.triggered.connect(self.change_light_style)
        return light_act

    def create_polycortex_info_btn(self):
        polycortex_icon = QIcon(self.polycortex_logo_path_alpha_background)
        polyCortex_actn = QAction(polycortex_icon, 'PolyCortex', self.main_window)
        polyCortex_actn.setStatusTip('Get information about PolyCortex Society')
        polyCortex_actn.triggered.connect(self.show_polycortex_info_page)
        self.w = None
        return polyCortex_actn

    def show_polycortex_info_page(self):
        self.polycortex_info_win = MyPopUp()
        self.polycortex_info_win.setGeometry(QRect(100, 200, 400, 200))
        self.polycortex_info_win.show()

    def change_light_style(self):
        self.main_window.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())



