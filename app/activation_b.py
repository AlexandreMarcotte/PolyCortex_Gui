from PyQt5.QtWidgets import *
from functools import partial

def btn(name, layout, pos, func_conn=None, color=None, toggle=False, tip=None,
        max_width=1200, min_width=16):
    b = QPushButton(name)
    b.setStyleSheet('background-color: {}; min-width: {}px;'
                    'max-width: {}px'.format(color, min_width, max_width))
    if tip: 
        b.setToolTip(tip)
    if toggle:
        b.setCheckable(True)
    if func_conn:
        b.clicked.connect(partial(func_conn))
    layout.addWidget(b, *pos)
    
    
