from V2.GUI.tabs.live_graph_tab.view.docks.inner_dock import InnerDock
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


class BannerDock(InnerDock):
    def __init__(self, size=(1, 1), external_layout=None):
        super().__init__(
            name='Banner', size=size, toggle_btn=True, add_dock_area=False,
            set_scroll=False, external_layout=external_layout, b_checked=False)
        self._add_banners()

    def _add_banners(self):
        # Polycortex
        polycortex_banner = QLabel()
        polycortex_banner.setPixmap(
            QtGui.QPixmap('./GUI/img/polycortex_banner.png'))
        self.inner_layout.addWidget(polycortex_banner, 0, 0)
        # OpenBci
        open_bci_banner = QLabel()
        open_bci_banner.setPixmap(
            QtGui.QPixmap('GUI/img/openbci_banner.png'))
        self.inner_layout.addWidget(open_bci_banner, 0, 1)

