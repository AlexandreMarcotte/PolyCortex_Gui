# game options
TITLE = 'my game'
WIDTH = 650
HEIGHT = 1014
# SCREEN_WIDTH =
FPS = 70

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5

# Starting platforms
p_size = [(400, 20)]


def grnd_pos(pos):
    return HEIGHT - pos

# (x, y, w, thickness)
p4 = (0, grnd_pos(200), *p_size[0])
p3 = (100, grnd_pos(400), *p_size[0])
p2 = (200, grnd_pos(600), *p_size[0])
p1 = (300, grnd_pos(800), *p_size[0])
base = (0, HEIGHT - 40, WIDTH, 40)

PLATFORM_LIST = [base, p1, p2, p3, p4]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)