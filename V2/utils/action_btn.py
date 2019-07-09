from PyQt5.QtWidgets import *


class Btn(QPushButton):
    def __init__(self, name, color=None, toggle=False, tip=None,
                 max_width=1200, min_width=15, max_height=None,
                 txt_color=None, font_size=11):
        super().__init__(name)

        self._name = name
        self._max_width = max_width
        self._min_width = min_width
        self._max_height = max_height
        self._color = color
        self._txt_color = txt_color
        self._font_size = font_size
        self._tip = tip
        self._toggle = toggle

        self.set_size()
        self.set_style()
        self.set_tip()
        self.set_toggle()
        # if action:
        #     self.clicked.connect(partial(action.show_action))
        # if func_conn:
        #     self.clicked.connect(partial(func_conn))
    def set_size(self):
        if self._name == 'Start':
            self._max_width = 85
            self._min_width = 85

        self.setMinimumWidth(self._min_width)
        self.setMaximumWidth(self._max_width)
        if self._max_height is not None:
            self.setMaximumHeight(self._max_height)

    def set_style(self):
        if self._txt_color:
            self.setStyleSheet(
                f'''background-color: {self._color}; color: {self._txt_color}; 
                    font-size: {self._font_size}pt;''')
        else:
            self.setStyleSheet(
                f'''background-color: {self._color}; font-size: {self._font_size}pt''')

    def set_color(self, color):
        self.setStyleSheet(f'background-color: {color}; font-size: 11pt;')

    def set_tip(self):
        if self._tip is not None:
            self.setToolTip(self._tip)

    def set_toggle(self):
        if self._toggle:
            self.setCheckable(True)

