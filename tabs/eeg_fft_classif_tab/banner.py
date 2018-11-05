from PyQt5.QtWidgets import *
from PyQt5 import QtGui

def add_banner(main_window, layout):
    # Polycortex
    polycortex_banner = QLabel(main_window)
    polycortex_banner.setPixmap(QtGui.QPixmap('./logo/polycortex_banner.png'))
    layout.addWidget(polycortex_banner, 0, 0, 1, 1)
    # OpenBci
    open_bci_banner = QLabel(main_window)
    open_bci_banner.setPixmap(QtGui.QPixmap('./logo/openbci_banner.png'))
    layout.addWidget(open_bci_banner, 0, 1, 1, 1)