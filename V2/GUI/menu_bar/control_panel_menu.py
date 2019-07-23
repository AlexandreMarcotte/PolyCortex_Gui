# -- General Packages --
from PyQt5.QtWidgets import *
# -- My Packages --
from .menu_action import MenuAction


class ControlPanelMenu(QMenu):
    def __init__(self, main_window):
        super().__init__('System Control Panel')

        MenuAction.set_model = \
            main_window.table_widget.live_graph_tab.model

        # Synthetic_data
        self.stream_from_synthetic_data = MenuAction(
            name='Synthetic data', icon_path='./GUI/img/sinus.png')
        self.addAction(self.stream_from_synthetic_data)
        # File
        self.stream_from_file = MenuAction(
            name='File', icon_path='./GUI/img/file.png')
        self.addAction(self.stream_from_file)
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



        # self.stream_from_synthetic_data = StreamFromFileAction('From Synthetic data')
        # self.addAction(self.stream_from_file)


    """
    def add_action_to_control_panel(self):
        ## Create menu action
        # OpenBCI
        self.openbci_actn = MenuAction(
            name='OpenBCI', gv=self.gv, icon_path='./img/openbci_logo.png',
            status_tip='Stream data from Openbci...', shortcut='Ctrl+O' )
        self.controlPanel.addAction(self.openbci_actn)
        # PCB
        self.pcb_actn = MenuAction(
            name="PolyCortex's PCB", gv=self.gv,
            icon_path='./img/polycortex_logo_alpha_background.png',
            status_tip='Stream the data from PolyCortex PCB' )
        self.controlPanel.addAction(self.pcb_actn)
        # Muse
        self.muse_actn = MenuAction(
            name='Muse', gv=self.gv, icon_path='./img/muse.png',
            status_tip='Stream data from Muse headband...' )
        self.controlPanel.addAction(self.muse_actn)
        # Fake data
        self.synthetic_data_actn = MenuAction(
            name='Synthetic data', gv=self.gv, icon_path='./img/sinus.png',
            status_tip='Stream data from artificially generated data...')
        self.controlPanel.addAction(self.synthetic_data_actn)
        # From File
        self.menu_file = MenuFile(
            name='File', gv=self.gv, main_window=self.main_window,
            status_tip='Stream data from previously saved file...')
        self.controlPanel.addMenu(self.menu_file)
    """
