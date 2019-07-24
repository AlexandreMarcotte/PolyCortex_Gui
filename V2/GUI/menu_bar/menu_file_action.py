# -- General Packages --
from functools import partial
# -- My Packages --
from .menu_action import MenuAction
from V2.utils.select_file import select_file
from V2.general_settings import GeneralSettings


class MenuFileAction(MenuAction):
    def __init__(self, name, main_window=None, icon_path=None,
                 status_tip='', shortcut=None):

        self.stream_path = None

        super().__init__(
            name=name, main_window=main_window, icon_path=icon_path,
            status_tip=status_tip, shortcut=shortcut)

    def connect_to_select_stream(self):
        self.triggered.connect(self.set_stream_path)
        self.triggered.connect(
            partial(self.model.pipeline.update_streamer, self.name))

    def set_stream_path(self):
        f_name = select_file(self.main_window, open=True)
        if f_name:
            GeneralSettings.file.stream_path = f_name
