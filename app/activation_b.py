from PyQt5.QtWidgets import *
from functools import partial
from app.colors import *


class btn:
    def __init__(self, name, layout, pos, size=(1, 1), func_conn=None,
                 action=None, color=None, toggle=False, tip=None,
                 max_width=1200, min_width=15, txt_color=None):
        self.b = QPushButton(name)
        self.b.setMinimumWidth(min_width)
        self.b.setMaximumWidth(max_width)
        if txt_color:
            self.b.setStyleSheet(f'background-color: {color}; color: {white}; font-size: 11pt;')
        else:
            self.b.setStyleSheet(f'background-color: {color}; font-size: 11')
        if tip:
            self.b.setToolTip(tip)
        if toggle:
            self.b.setCheckable(True)
        if action:
            self.b.clicked.connect(partial(action.show_action))
        if func_conn:
            self.b.clicked.connect(partial(func_conn))

        layout.addWidget(self.b, *pos, *size)

    def set_color(self, color):
        self.b.setStyleSheet(f'background-color: {color}; font-size: 11pt;')

