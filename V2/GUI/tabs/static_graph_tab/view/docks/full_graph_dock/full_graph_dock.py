from V2.GUI.tabs.inner_dock import InnerDock


class FullGraphDock(InnerDock):
    def __init__(self, ch):
        super().__init__(
            f'{ch+1}', toggle_btn=False, hide_title=False,
            auto_orientation=True)
        self.setOrientation(o='vertical')
