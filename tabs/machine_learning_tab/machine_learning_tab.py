from PyQt5.QtWidgets import *
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from PyQt5 import QtCore
from app.rotated_button import RotatedButton


class MachineLearningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.create_tab()
        self.tool_dock = self.create_tool_dock()
        self.create_txt_dock()

    def create_tab(self):
        layout = QHBoxLayout(self)
        self.dock_area = DockArea()
        layout.addWidget(self.dock_area)
        self.setLayout(layout)

    def create_txt_dock(self):
        # txt
        txt_dock = Dock('Results')
        self.dock_area.addDock(txt_dock, 'right')
        txt_layout = pg.LayoutWidget()
        txt_dock.addWidget(txt_layout)
        txt = QTextEdit()
        txt_layout.addWidget(txt, 0, 1)
        # btn
        b = RotatedButton('Settings', orientation='east')
        # b.setMaximumWidth(20)
        b.setCheckable(True)
        b.clicked.connect(self.open_tool_box)
        txt_layout.addWidget(b, 0, 0)

    def create_tool_dock(self):
        tool_dock = Dock('tool dock')
        tool_dock.hideTitleBar()
        self.dock_area.addDock(tool_dock, 'left')
        tool_layout = pg.LayoutWidget()
        tool_dock.addWidget(tool_layout)

        tb = QToolBox()

        self.create_optimizer_toolbox(tb)
        self.create_neural_network_layer_toolbox(tb)

        tool_layout.addWidget(tb)

        return tool_dock

    def create_optimizer_toolbox(self, tb):
        # Optimizer layout
        optimizer_layout = pg.LayoutWidget()
        optimizer_layout.addWidget(QPushButton('Test123'))
        optimizer_layout.addWidget(QTextEdit('Here I go again'))
        tb.addItem(optimizer_layout, 'Optimizer')
        # tb.addItem(QPushButton('Test2'))

    def create_neural_network_layer_toolbox(self, tb):
        tb.addItem(QPlainTextEdit(), f'Layer #1')

    # @QtCore.pyqtSlot(bool)
    def open_tool_box(self, checked):
        if checked:
            print('open tool box')
            self.tool_dock.show()
        else:
            self.tool_dock.hide()


