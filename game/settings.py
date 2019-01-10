# game options
TITLE = 'my game'
WIDTH = 600
HEIGHT = 600
FPS = 70

# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.5

# Starting platforms
# (x, y, w, thickness)
PLATFORM_LIST = [
        (0, HEIGHT - 40, WIDTH, 40), (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
        (125, HEIGHT - 350, 300, 20), (350, 200, 400, 20), (175, 100, 200, 20)]

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)