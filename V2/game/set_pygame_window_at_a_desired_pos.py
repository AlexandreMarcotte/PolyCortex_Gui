import pygame as pg
import os


def set_pygame_window_at_a_desired_pos():
    pg.display.set_mode((0, 0), pg.FULLSCREEN)
    screen_info = pg.display.Info()
    SCREEN_W = screen_info.current_w
    SCREEN_H = screen_info.current_h
    pg.quit()
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{SCREEN_W},{SCREEN_H}'
    return SCREEN_W, SCREEN_H


