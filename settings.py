import pygame
from pyglet import font

font.add_file('gui/main.ttf')
mainFont = font.load('gui/main.ttf', 16)

pygame.init()

monitor = pygame.display.Info()
WIDTH = monitor.current_w
HEIGHT = monitor.current_h
MAX_FPS = 250
PAUSE = False
clock = pygame.time.Clock()

FOV = 100
RENDER_DISTANCE = 100

CHUNKS_RENDER_DISTANCE = 100
CHUNK_SIZE = (2, 50, 2)
