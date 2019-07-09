# -- General Packages --
from PyQt5.QtWidgets import QToolBar
# -- My Packages --
from .toolbar_actions.dark_mode_action import DarkModeAction
from .toolbar_actions.exit_action import ExitAction
from .toolbar_actions.polycortex_info_action import PolycortexInfoAction


class ToolBar(QToolBar):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self._add_actions(main_window)

    def _add_actions(self, main_window):
        self.addAction(ExitAction(self, main_window))
        self.addAction(DarkModeAction(self, main_window))
        self.addAction(PolycortexInfoAction(self))


