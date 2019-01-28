from PyQt5.QtWidgets import *
from functools import partial
from app.colors import *


class btn:
    def __init__(self, name, layout, pos, size=(1, 1), func_conn=None,
                 action=None, color=None, toggle=False, tip=None,
                 max_width=1200, min_width=15, max_height=None,
                 txt_color=None, font_size=11):
        if name == 'Start':
            max_width = 85
            min_width = 85

        self.b = QPushButton(name)
        self.b.setMinimumWidth(min_width)
        self.b.setMaximumWidth(max_width)
        if max_height is not None:
            self.b.setMaximumHeight(max_height)
        if txt_color:
            self.b.setStyleSheet(
                    f'''background-color: {color}; color: {txt_color}; 
                        font-size: {font_size}pt;''')
        else:
            self.b.setStyleSheet(
                    f'''background-color: {color}; font-size: {font_size}pt''')
        if tip is not None:
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

