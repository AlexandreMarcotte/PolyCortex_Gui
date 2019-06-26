from PyQt5.QtWidgets import *
# --My packages--
from .model import Model
from .view import View


class LiveGraphTabController:
    def __init__(self):
        self._model = Model()
        self._view = View(self._model)


