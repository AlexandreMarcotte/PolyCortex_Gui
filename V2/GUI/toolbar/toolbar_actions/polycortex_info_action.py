from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from V2.utils.pop_up import PopUp


class PolycortexInfoAction(QAction):
    def __init__(self, tool_bar):
        polycortex_logo_path = 'GUI/img/polycortex_logo_alpha_background.png'
        icon = QIcon(polycortex_logo_path)
        super().__init__(icon, 'PolyCortex', tool_bar)

        self.setStatusTip('Get information about PolyCortex Society')
        self.triggered.connect(self.show_polycortex_info_page)
        # self.w = None

    def show_polycortex_info_page(self):
        self.polycortex_info_win = PopUp()
        self.polycortex_info_win.show()
