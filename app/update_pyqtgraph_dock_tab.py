# from: https://gist.github.com/matmr/72487a03da95b99db6ae


def update_style_patched(self):
    r = '3px'
    if self.dim:
        fg = '#FFFFFF'
        bg = '#1E82AA'
        border = '#1E82AA'
    # Clicked
    else:
        fg = '#FFFFFF'
        bg = '#46AFD2'
        border = '#46AFD2'

    if self.orientation == 'vertical':
        self.vStyle = """DockLabel {
            background-color : %s;
            color : %s;
            border-top-right-radius: 0px;
            border-top-left-radius: %s;
            border-bottom-right-radius: 0px;
            border-bottom-left-radius: %s;
            border-width: 0px;
            border-right: 2px solid %s;
            padding-top: 3px;
            padding-bottom: 3px;
            font-size: 14px;
        }""" % (bg, fg, r, r, border)
        self.setStyleSheet(self.vStyle)
    else:
        self.hStyle = """DockLabel {
            background-color : %s;
            color : %s;
            border-top-right-radius: %s;
            border-top-left-radius: %s;
            border-bottom-right-radius: 0px;
            border-bottom-left-radius: 0px;
            border-width: 0px;
            border-bottom: 2px solid %s;
            padding-left: 13px;
            padding-right: 13px;
            font-size: 14px
        }""" % (bg, fg, r, r, border)
        self.setStyleSheet(self.hStyle)


