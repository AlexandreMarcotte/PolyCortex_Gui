from PyQt5.QtWidgets import *
from functools import partial

def btn(name, layout, pos, func_conn=None, action=None, color=None,
        toggle=False, tip=None, max_width=1200, min_width=16):
    b = QPushButton(name)
    b.setStyleSheet(f'background-color: {color}; min-width: {min_width}px;'
                    f'max-width: {max_width}px')
    if tip: 
        b.setToolTip(tip)
    if toggle:
        b.setCheckable(True)
    if action:
        b.clicked.connect(partial(action.show_action))
    if func_conn:
        b.clicked.connect(partial(func_conn))
    layout.addWidget(b, *pos)