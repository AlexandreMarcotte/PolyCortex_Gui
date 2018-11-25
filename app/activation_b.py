from PyQt5.QtWidgets import *
from functools import partial
from app.colors import *

def btn(name, layout, pos, size=(1, 1), func_conn=None, action=None, color=None,
        toggle=False, tip=None, max_width=1200, min_width=16, txt_color=None):
    b = QPushButton(name)
    if txt_color:
        b.setStyleSheet(f'background-color: {color}; color: {white};'
                        f'min-width: {min_width}px; max-width: {max_width}px')
    else:
        b.setStyleSheet(f'background-color: {color};'
                        f'min-width: {min_width}px; max-width: {max_width}px')
    if tip: 
        b.setToolTip(tip)
    if toggle:
        b.setCheckable(True)
    if action:
        b.clicked.connect(partial(action.show_action))
    if func_conn:
        b.clicked.connect(partial(func_conn))

    layout.addWidget(b, *pos, *size)