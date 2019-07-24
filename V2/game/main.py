# Creativity game

from V2.game.game import Game
# multithreading
import threading


class RunGame(threading.Thread):
    def __init__(self, main_window, test_mode=True):
        super().__init__()
        self.g = Game(test_mode=test_mode, main_window=main_window)
        self.g.show_start_screen()

    def run(self):
        while self.g.running:
            self.g.new()
            self.g.show_go_screen()


if __name__ == '__main__':
    run_game = RunGame()
    run_game.start()

