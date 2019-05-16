#--General Packages--
from PyQt5.QtWidgets import *

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from pyqtgraph.dockarea import *

from pynput import keyboard
from random import randint
# --My Packages--
from .robotic_arm.robotic_arm import RoboticArmDock


class Game3DTab(QWidget):
    def __init__(self):
        super().__init__()
        # Create the tab itself
        self.create_tab()

    def create_tab(self):
        self.layout = QHBoxLayout(self)
        self.area = DockArea()
        self.layout.addWidget(self.area)
        # Collect events until released
        game_3d_dock = Game3DDock(self)
        robotic_arm_dock = RoboticArmDock(self, game_3d_dock.dock)

        listen_keybr = keyboard.Listener(
                on_press=game_3d_dock.on_press,
                on_release=game_3d_dock.on_release)
        # Uncomment if you want to play the game
        # listen_keybr.start()
        self.setLayout(self.layout)


class Game3DDock:
    def __init__(self, tab_w):
        self.tab_w = tab_w

        self.key_pressed = ''
        self.dock = Dock('Mini Game 3D')
        self.tab_w.area.addDock(self.dock)

        self.view = self.init_view()
        self.init_character()
        # food
        self.food_list = []
        self.N_FOOD = 5
        self.init_food()

        self.mvt_timer = self.init_mvt_timer()
        self.contact_timer = self.init_contact_timer()

    def init_mvt_timer(self):
        # Update the position of the character
        mvt_timer = QtCore.QTimer()
        mvt_timer.timeout.connect(self.update_character_pos)
        mvt_timer.start(5)
        return mvt_timer

    def init_contact_timer(self):
        # look if there is a contact between character and food
        contact_timer = QtCore.QTimer()
        contact_timer.timeout.connect(self.contact)
        contact_timer.start(50)
        return contact_timer

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

    def init_view(self):
        v = gl.GLViewWidget()
        self.dock.addWidget(v)
        v.setWindowTitle('pyqtgraph example: GL Shaders')
        v.setCameraPosition(distance=60, azimuth=-90)
        g = gl.GLGridItem()
        g.scale(2, 2, 1)
        v.addItem(g)
        return v

    def init_character(self):
        self.x_pos = -20
        self.y_pos = -20
        self.character_height = 1.3
        md = gl.MeshData.sphere(rows=10, cols=30)
        self.m = gl.GLMeshItem(
                meshdata=md, smooth=True, shader='normalColor',
                glOptions='opaque')
        self.m.translate(self.x_pos, self.y_pos, self.character_height)
        self.m.scale(
                self.character_height, self.character_height,
                self.character_height)
        self.view.addItem(self.m)

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
            self.view.addItem(food.mesh)

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


