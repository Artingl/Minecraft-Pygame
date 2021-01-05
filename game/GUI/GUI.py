import pyglet
from settings import *


class GUI:
    def __init__(self):
        print("Init GUI class...")

        self.GUI_TEXTURES = {}
        self.shows = {}

        self.lopacity = 255
        self.label = pyglet.text.Label("",
                                       font_name='Minecraft Rus',
                                       color=(255, 255, 255, 255),
                                       font_size=17,
                                       x=WIDTH // 2, y=90, anchor_x='center')

    def showText(self, text):
        self.label.text = text
        self.lopacity = 255

    def update(self):
        self.lopacity -= 1
        if self.lopacity < 0:
            self.lopacity = 1
        else:
            self.label.set_style("color", (255, 255, 255, self.lopacity))
            self.label.draw()

        for i in self.shows.values():
            i[0].blit(*i[1])

    def addGuiElement(self, image, pos):
        self.shows[image] = [self.GUI_TEXTURES[image], pos]
