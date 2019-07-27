# --My Packages--
from V2.GUI.tabs.inner_dock import InnerDock


class FilterDock(InnerDock):
    def __init__(self, external_layout=None):
        super().__init__(
            name='Filter', toggle_btn=True, b_checked=False,
            external_layout=external_layout)

