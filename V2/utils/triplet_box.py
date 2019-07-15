from V2.utils.clickable_line_edit import ClickableLineEdit
from V2.utils.create_txt_label import Label
from V2.utils.colors import *


class TripletBox:
    def __init__(self, layout, name, pos, colors=None):
        self.layout = layout
        self.name = name
        self._pos = pos

        self._N_COMBO_BOX = 3

        self.add_txt_label()
        self._add_triplet_txt_box(pos, layout, colors)

    def add_txt_label(self):
        pos_label = Label(self.name)
        self.layout.addWidget(pos_label, 0, self._pos[1], 1, self._N_COMBO_BOX)
        pos_label.setStyleSheet(f'''font-weight: 430;
                                font-size: 10pt;
                                background-color: {combobox_grey}''')

    def _add_triplet_txt_box(self, pos, layout, colors=None):
        col = pos[1]
        self.all_l_e = []
        for i in range(self._N_COMBO_BOX):
            l_e = ClickableLineEdit(i, self.name)
            if colors is not None:
                l_e.setStyleSheet(
                    f"""border-style: solid; 
                            border-color: {colors[i]}; 
                            border-width: 1px 1px 1px 1px;
                         """)
            l_e.setMaximumWidth(30)
            layout.addWidget(l_e, 1, col+i)
            self.all_l_e.append(l_e)
