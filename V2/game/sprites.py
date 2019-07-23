# Sprite classes for platform game
import pygame as pg
from game.settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, gv, test_mode=False):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.gv = gv
        self.test_mode = test_mode

        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, dokill=False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -15

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        # test mode
        if self.test_mode:
            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC * 2
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC * 2

        else:
            if self.gv.class_detected[0] == 0:
                self.acc.x = -PLAYER_ACC * 4
            if self.gv.class_detected[1] == 0:
                self.acc.x = PLAYER_ACC * 4

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + PLAYER_GRAV * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y