# Creativity game
import pygame as pg
import random
from game.settings import *
from game.sprites import *
import os
# multithreading
import threading


def set_pygame_window_at_a_desired_pos():
    pg.display.set_mode((0, 0), pg.FULLSCREEN)
    screen_info = pg.display.Info()
    SCREEN_W = screen_info.current_w
    SCREEN_H = screen_info.current_h
    pg.quit()
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{SCREEN_W},{SCREEN_H}'
    return SCREEN_W, SCREEN_H


class Game:
    def __init__(self, gv, test_mode=False):
        """
        Initialize game window, etc
        """
        self.gv = gv
        self.test_mode = test_mode

        SCREEN_W, SCREEN_H = set_pygame_window_at_a_desired_pos()
        pg.init()
        pg.mixer.init()
        pg.display.set_mode((WIDTH, HEIGHT))

        self.screen = pg.display.set_mode(
                (WIDTH, HEIGHT))

        if not test_mode:
            self.gv.openbci_gui.setGeometry(
                    0, 0, SCREEN_W - WIDTH, HEIGHT)

        pg.display.set_caption('EMG Platformer')
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = None
        self.playing = False

        self.itt = 0

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        # player
        self.player = Player(self, self.gv, test_mode=self.test_mode)
        self.all_sprites.add(self.player)
        # platform
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(
                    self.player, self.platforms, dokill=False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 1
                self.player.vel.y = 0

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.running = False

            self.itt += 1
            if self.test_mode:
                print('here')
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.player.jump()
            else:
                if self.gv.class_detected[0] == 1:
                    print(self.gv.class_detected[0])
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

   
class RunGame(threading.Thread):
    def __init__(self, gv):
        super().__init__()
        self.g = Game(gv, test_mode=True)
        self.g.show_start_screen()

    def run(self):
        while self.g.running:
            self.g.new()
            self.g.show_go_screen()


if __name__ == '__main__':
    gv = []
    run_game = RunGame(gv)
    run_game.start()

