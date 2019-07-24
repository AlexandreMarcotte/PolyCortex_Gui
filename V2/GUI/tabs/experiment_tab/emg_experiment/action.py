import pyqtgraph as pg


class Action:
    def __init__(self, actn_txt, wait_txt, y_pos, x_pos, color='#FF0'):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.actn_txt = actn_txt
        self.wait_txt = wait_txt
        self.color = color
        self.plot = None
        self.wait = True

        self.init_action()

    def init_action(self):
        self.plot = pg.TextItem(
                anchor=(0.5, 1), angle=0, border='w', fill=(0, 0, 255, 100))
        self.html = self.set_html(14, self.actn_txt, self.color, self.wait_txt)
        self.plot.setHtml(self.html)
        self.plot.setPos(self.x_pos, self.y_pos)

    def activate_html(self):
        """Change the color  and text of the action text to indicate it's
           activation"""
        self.html = self.set_html(16, self.actn_txt, color='#0FF', wait_txt='NOW!')
        self.plot.setHtml(self.html)

    def set_html(self, txt_size, actn_txt, color, wait_txt):
        return f"""<div style="text-align: center">
                   <span style="color: #FFF;">{actn_txt}
                   </span><br><span style="color: {color};
                   font-size: {txt_size}pt;">{wait_txt}</span></div>"""
        