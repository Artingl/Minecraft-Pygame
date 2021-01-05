import timeit

import pygame
from pyglet import font

font.add_file('gui/main.ttf')
mainFont = font.load('gui/main.ttf', 15)

pygame.init()

monitor = pygame.display.Info()
WIDTH = 927  # monitor.current_w
HEIGHT = 566  # monitor.current_h
MAX_FPS = 100
PAUSE = True
IN_MENU = True
MC_VERSION = "1.0 release"
clock = pygame.time.Clock()

FOV = 100
RENDER_DISTANCE = 100

CHUNKS_RENDER_DISTANCE = 900
CHUNK_SIZE = (2, 50, 2)
