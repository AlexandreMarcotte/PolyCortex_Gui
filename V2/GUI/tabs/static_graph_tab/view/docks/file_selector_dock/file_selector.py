from V2.GUI.tabs.inner_dock import InnerDock


class FileSelectorDock(InnerDock):
    def __init__(self, external_layout):
        super().__init__(
            'File Selector', toggle_btn=False, b_pos=(0, 0), hide_title=False,
            auto_orientation=True, external_layout=external_layout,
            fixed_height=110)
        self.setOrientation(o='vertical')
