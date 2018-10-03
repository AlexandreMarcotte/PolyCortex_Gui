# Creativity game
import pygame as pg
import random
from game.settings import *
from game.sprites import *
# multithreading 
import threading


class Game:
    def __init__(self):
        """
        Initialize game window, etc
        """
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('My Game')
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = None
        self.playing = False

    def new(self):
        # start a new game
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        # player
        self.player = Player(self)
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
            hits = pg.sprite.spritecollide(self.player, self.platforms,
                                           dokill=False)
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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
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
    def __init__(self):
        super().__init__()
        self.g = Game()
        self.g.show_start_screen()

    def run(self):
        while self.g.running:
            self.g.new()
            self.g.show_go_screen()


if __name__ == '__main__':
    run_game = RunGame()
    run_game.start()

