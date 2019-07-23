# -- General Packages --
from PyQt5.QtWidgets import *
# -- My Packages --
from .menu_action import MenuAction
from .menu_file import MenuFile


class ControlPanelMenu(QMenu):
    def __init__(self, main_window):
        super().__init__('System Control Panel')

        MenuAction.model = \
            main_window.table_widget.live_graph_tab.model

        # Synthetic_data
        self.stream_from_synthetic_data = MenuAction(
            name='Synthetic data', icon_path='./GUI/img/sinus.png')
        self.addAction(self.stream_from_synthetic_data)
        # OpenBci
        self.stream_from_openbci = MenuAction(
            name='OpenBci', icon_path='./GUI/img/openbci_logo.png')
        self.addAction(self.stream_from_openbci)
        # Muse
        self.stream_from_muse = MenuAction(
            name='Muse', icon_path='./GUI/img/muse.png')
        self.addAction(self.stream_from_muse)
        # PCB
        self.stream_from_pcb = MenuAction(name='PCB')
        self.addAction(self.stream_from_pcb)
        # File
        self.stream_from_file = MenuFile(
            name='File', icon_path='./GUI/img/file.png')
        self.addMenu(self.stream_from_file)
