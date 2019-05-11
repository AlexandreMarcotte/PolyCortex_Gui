from PyQt5.QtGui import QIcon
from PyQt5 import QtGui


class MenuAction(QtGui.QAction):
    def __init__(self, name, icon_path, status_tip):
        super().__init__()

        self.name = name

        icon = QIcon(icon_path)
        self.setIcon(icon)
        self.setIconText(name)

        self.setStatusTip(status_tip)


    # def create_actn(self):
    #     actn = QtGui.QAction(
    #         QIcon(self.sinus_logo_path), 'Synthetic data')
    #     actn.setStatusTip(
    #         'Stream data from artificially generated data...')
    #     actn.name = 'Stream from synthetic data'
    #     return actn
