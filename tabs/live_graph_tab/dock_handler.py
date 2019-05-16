from PyQt5 import QtGui
import pyqtgraph as pg
from PyQt5.QtWidgets import *
from pyqtgraph.dockarea import *


class DockHandler:
    def __init__(self, name, tab, menu, DockObj, param, pos, related_dock=None,
                 size=(1, 1), hide_title=False, scroll=False):
        self.name = name
        self.DockObj = DockObj
        self.tab = tab
        self.param = param
        self.pos = pos
        self.related_dock = related_dock
        self.size = size
        self.hide_title = hide_title
        self.scroll = scroll

        self.first_time = True

        self.dock = self.init_dock()

        self.dock_obj = DockObj(*param)
        if name == 'EEG':
            x = self.dock_obj.regions

        self.state = 'checked'

        self.check_actn = QtGui.QAction(name, tab, checkable=True)
        self.check_actn.setChecked(True)
        self.check_actn.triggered.connect(self.open_close_dock)
        self.check_actn.setStatusTip(f'Check {name} to open this dock...')

        menu.addAction(self.check_actn)

    def init_dock(self):
        dock = Dock(self.name, size=self.size)
        try:
            self.tab.area.addDock(dock, self.pos, self.related_dock)
        except AttributeError as e:  # The related dock as been deleted
            print('except', e)
            self.tab.area.addDock(dock, 'bottom')
        layout = pg.LayoutWidget()
        if self.scroll:
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            dock.addWidget(scroll)
            scroll.setWidget(layout)
        else:
            dock.addWidget(layout)
        if self.hide_title:
            dock.hideTitleBar()

        if self.first_time:
            self.param.append(layout)
            self.first_time = False
        else:
            self.param.pop()
            self.param.append(layout)

        return dock

    def open_close_dock(self):
        if self.state == 'checked':
            self.dock.close()
            self.state = 'unchecked'

        elif self.state == 'unchecked':
            # self.tab.init_tab_w()
            self.dock = self.init_dock()
            self.dock_obj = self.DockObj(*self.param)
            self.tab.setLayout(self.tab.layout)
            self.state = 'checked'
            if self.name == 'EEG':
                self.tab.eeg.dock_obj.set_saver(self.tab.saving.dock_obj)
