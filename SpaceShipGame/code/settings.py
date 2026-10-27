from pyray import *
from raylib import *
from random import randint, uniform
from pathlib import Path



WINDOW_WIDTH, WINDOW_HEIGHT = 720, 480
BG_COLOR = (15,10,25,255)
PLAYER_SPEED = 500
LASER_SPEED = 600
METEOR_SPEED_RANGE = [300,400]
METEOR_TIMER_DURATION = 0.4
FONT_SIZE = 120
