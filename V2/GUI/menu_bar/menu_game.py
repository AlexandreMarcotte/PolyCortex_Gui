from V2.game.main import RunGame
from PyQt5 import QtGui
from PyQt5.QtWidgets import *


class MenuGame(QMenu):
    def __init__(self, name, main_window):
        super().__init__()
        self.main_window = main_window

        self.setTitle(name)

        self.add_action()

    def add_action(self):
        # ---Start game---
        self.start_game = QtGui.QAction('Start platformer game...')
        self.start_game.setStatusTip('Press to start the mini game...')
        self.start_game.triggered.connect(self.start_the_game)
        self.addAction(self.start_game)

    def start_the_game(self):
        """Start the miniGame"""
        run_game = RunGame(test_mode=True, main_window=self.main_window)
        run_game.start()
