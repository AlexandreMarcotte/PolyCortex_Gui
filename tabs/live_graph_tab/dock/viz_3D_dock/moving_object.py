# --General Packages--
from pynput import keyboard
from PyQt5 import QtCore
import numpy as np
from numpy import array as arr


class MovingObject:
    def __init__(self, gv, listening_process):
        self.gv = gv
        self.listening_process = listening_process

        self.pos = np.array([0, 0, 0], dtype='float64')                        #TODO: ALEXM: Changer pour un vector

        self.pointer_actn = {'d': arr([0.2, 0, 0]),
                             'a': arr([-0.2, 0, 0]),
                             's': arr([0, 0.2, 0]),
                             'w': arr([0, 0.2, 0]),
                             'r': arr([0, 0, 0.3]),
                             'f': arr([0, 0, -0.3])
                            }

        self.key_pressed = ''
        if listening_process:
            self.listen_keybr = self.start_listening_process()

    def create_timer(self, slot):
        timer = QtCore.QTimer()
        timer.timeout.connect(slot)
        return timer

    def start_listening_process(self):
        listen_keybr = keyboard.Listener(
                on_press=self.on_press, on_release=self.on_release)
        listen_keybr.start()
        return listen_keybr

    def on_press(self, key):
        try:
            self.key_pressed = key.char
        except AttributeError:
            self.key_pressed = key

    def on_release(self, key):
        pass
        if key == keyboard.Key.esc:
            self.listen_keybr.start()
