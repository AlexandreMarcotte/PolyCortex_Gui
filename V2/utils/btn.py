from PyQt5.QtWidgets import QPushButton
from V2.utils.colors import *


class Btn(QPushButton):
    def __init__(self, name, color=dark_blue_tab, toggle=False, tip=None,
                 max_width=1200, min_width=15, max_height=None,
                 txt_color=white, font_size=11):
        super().__init__(name)

        self._set_size(name, max_width, min_width, max_height)
        self._set_style(color, txt_color, font_size)
        self.set_tip(tip)
        self.set_toggle(toggle)

    def _set_size(self, name, max_width, min_width, max_height):
        if name == 'Start':
            max_width = 85
            min_width = 85

        self.setMinimumWidth(min_width)
        self.setMaximumWidth(max_width)
        if max_height is not None:
            self.setMaximumHeight(max_height)

    def _set_style(self, color, txt_color, font_size):
        if txt_color:
            self.setStyleSheet(
                f'''background-color: {color}; color: {txt_color}; 
                    font-size: {font_size}pt;''')

    def set_tip(self, tip):
        if tip is not None:
            self.setToolTip(tip)

    def set_toggle(self, toggle):
        if toggle:
            self.setCheckable(True)

