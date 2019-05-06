import pygame

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, pyqtSlot

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

# import pygame
from pynput import keyboard
import threading
from random import randint


class Game3DTab(QWidget):
    def __init__(self):
        super().__init__()
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.layout = QHBoxLayout(self)
        # Collect events until released
        game_3d = Game3D(self)
        listen_keybr = keyboard.Listener(
                on_press=game_3d.on_press, on_release=game_3d.on_release)
        # Uncomment if you want to play the game
        # listen_keybr.start()

        self.setLayout(self.layout)


class Game3D:
    def __init__(self, tab5):
        # Variables
        self.tab_w = tab5

        self.init_landscape()
        self.init_character()

        # food
        self.food_list = []
        self.N_FOOD = 5
        self.init_food()

        self.init_mvt_timer()

        self.init_contact_timer()

        self.key_pressed = ''

    def init_mvt_timer(self):
        # Update the position of the character
        self.mvt_timer = QtCore.QTimer()
        self.mvt_timer.timeout.connect(self.update_character_pos)
        self.mvt_timer.start(5)

    def init_contact_timer(self):
        # look if there is a contact between character and food
        self.contact_timer = QtCore.QTimer()
        self.contact_timer.timeout.connect(self.contact)
        self.contact_timer.start(50)

    def contact(self):
        for food in self.food_list:
            # x:
            low_x = food.x - food.height
            high_x = food.x + food.height
            # y:
            low_y = food.y - food.height
            high_y = food.y + food.height

            # Remove food if character is inside its boundaries
            if low_x <= self.x_pos <= high_x and low_y <= self.y_pos <= high_y:
                old_x = food.x
                old_y = food.y
                food.x = randint(-20, 20)
                food.y = randint(-20, 20)
                food.mesh.translate(food.x - old_x, 0, 0)
                food.mesh.translate(0, food.y - old_y, 0)

    def init_landscape(self):
        # self.app = QtGui.QApplication([])
        self.w = gl.GLViewWidget()
        self.tab_w.layout.addWidget(self.w)
        self.w.setWindowTitle('pyqtgraph example: GL Shaders')
        self.w.setCameraPosition(distance=60, azimuth=-90)
        g = gl.GLGridItem()
        g.scale(2, 2, 1)
        self.w.addItem(g)

    def init_character(self):
        self.x_pos = -20
        self.y_pos = -20
        self.character_height = 1.3
        md = gl.MeshData.sphere(rows=10, cols=30)
        self.m = gl.GLMeshItem(
            meshdata=md, smooth=True, shader='normalColor', glOptions='opaque')
        self.m.translate(self.x_pos, self.y_pos, self.character_height)
        self.m.scale(
            self.character_height, self.character_height, self.character_height)
        self.w.addItem(self.m)

    def update_character_pos(self):
        if self.key_pressed == 'l':
            self.m.translate(0.2, 0, 0)
            self.x_pos += 0.2
        if self.key_pressed == 'j':
            self.m.translate(-0.2, 0, 0)
            self.x_pos -= 0.2
        if self.key_pressed == 'i':
            self.m.translate(0, 0.3, 0)
            self.y_pos += 0.3
        if self.key_pressed == 'k':
            self.m.translate(0,-0.3, 0)
            self.y_pos -= 0.3

    def init_food(self):
        for food_no in range(self.N_FOOD):
            # Create a food object
            self.food_list.append(Food(height=1))

        for food in self.food_list:
            food.mesh.translate(food.x, food.y, food.height)
            self.w.addItem(food.mesh)

    def on_press(self, key):
        try:
            self.key_pressed = key.char
        except AttributeError:
            # print(f'special key {key} pressed')
            self.key_pressed = key

    def on_release(self, key):
        pass
        if key == keyboard.Key.esc:
            # Stop listener
            pass


class Food:
    def __init__(self, height):
        self.sphere = gl.MeshData.sphere(rows=10, cols=10)
        self.mesh = gl.GLMeshItem(
                meshdata=self.sphere, smooth=True, color=(1, 0, 0, 1),
                shader='edgeHilight', glOptions='opaque')
        self.height = height
        self.mesh.scale(1, 1, self.height)
        self.x = randint(-10, 10)
        self.y = randint(-10, 10)


