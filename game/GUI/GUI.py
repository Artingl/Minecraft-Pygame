import pyglet
from settings import *


class GUI:
    def __init__(self, gl):
        print("Init GUI class...")

        self.GUI_TEXTURES = {}
        self.shows = {}
        self.gl = gl

        self.lopacity = 255
        self.shadow_lbl = pyglet.text.Label("",
                                            font_name='Minecraft Rus',
                                            color=(56, 56, 56, self.lopacity),
                                            font_size=12,
                                            x=self.gl.WIDTH // 2, y=90, anchor_x='center')
        self.lbl = pyglet.text.Label("",
                                     font_name='Minecraft Rus',
                                     color=(255, 255, 255, self.lopacity),
                                     font_size=12,
                                     x=self.gl.WIDTH // 2 - 2, y=90 + 2, anchor_x='center')

    def showText(self, text):
        self.lbl.text = text
        self.shadow_lbl.text = text
        self.lopacity = 255

    def update(self):
        self.shadow_lbl.x = self.gl.WIDTH // 2 + 2
        self.lbl.x = self.gl.WIDTH // 2
        self.lopacity -= 1
        if self.lopacity < 0:
            self.lopacity = 1
        else:
            self.shadow_lbl.set_style("color", (56, 56, 56, self.lopacity))
            self.shadow_lbl.draw()
            self.lbl.set_style("color", (255, 255, 255, self.lopacity))
            self.lbl.draw()

        for i in self.shows.values():
            i[0].blit(*i[1])

    def addGuiElement(self, image, pos):
        self.shows[image] = [self.GUI_TEXTURES[image], pos]
