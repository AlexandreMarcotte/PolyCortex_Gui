from PyQt5.QtWidgets import *
from PyQt5 import QtGui


class Banner:
    def __init__(self, layout):
        # Polycortex
        polycortex_banner = QLabel()
        polycortex_banner.setPixmap(QtGui.QPixmap('./img/polycortex_banner.png'))
        layout.addWidget(polycortex_banner, 0, 0)
        # OpenBci
        open_bci_banner = QLabel()
        open_bci_banner.setPixmap(QtGui.QPixmap('./img/openbci_banner.png'))
        layout.addWidget(open_bci_banner, 0, 1)