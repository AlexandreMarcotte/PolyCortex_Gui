# --General Packages--
from pynput import keyboard
from PyQt5 import QtCore
import numpy as np
from numpy import array as arr


class MovingObject:
    def __init__(self, obj, update_func, listening_process):
        self.obj = obj
        self.update_func = update_func
        self.listening_process = listening_process

        self.update_func_types = {'update pos': self.update_pos,
                                  'move pointer': self.move_pointer,
                                  'move plane': self.move_plane}

        self.pos = np.array([0, 0, 0], dtype='float64')                                         #TODO: ALEXM: Changer pour un vector

        self.pointer_actn = {'d': arr([0.2, 0, 0]),
                         'a': arr([-0.2, 0, 0]),
                         's': arr([0, 0.2, 0]),
                         'w': arr([0, 0.2, 0]),
                         'r': arr([0, 0, 0.3]),
                         'f': arr([0, 0, -0.3])
                         }
        # self.plane_actn =

        self.create_timer()
        if listening_process:
            self.listen_keybr = self.start_listening_process()

    def move_pointer(self):
        try:
            mvt = self.pointer_actn[self.key_pressed]
            self.obj.item.translate(mvt[0], mvt[1], mvt[2])
            self.pos += mvt
        except KeyError:
            pass

    def move_plane(self):
        if self.key_pressed == 'd':
            self.obj.item.translate(1, 0, 0)

    def create_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_func_types[self.update_func])

    def update_pos(self):
        # self.item.translate(1000, 0, 0)
        pass

    def start_listening_process(self):
        listen_keybr = keyboard.Listener(on_press=self.on_press,
                                         on_release=self.on_release)
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

