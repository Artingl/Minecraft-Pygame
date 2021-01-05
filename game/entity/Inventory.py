import math
from random import randint

import pyglet
from pyglet.gl import GL_QUADS

from settings import *


class Inventory:
    def __init__(self, glClass):
        self.gl = glClass
        self.inventory = {}
        self.blocksLabel = {}
        self.activeInventory = 0
        self.heartAnimation = []

        ls = list(self.gl.inventory_textures.items())
        old = False
        for i in range(10):
            old = not old
            self.heartAnimation.append([0, '-' if old else '+'])
        for i in range(9*4 + 1):
            block = ls[i][0]
            if i == 0:
                block = "crafting_table"

            self.inventory[i] = [block, 64]
            self.blocksLabel[i] = pyglet.text.Label("0",
                                                    font_name='Minecraft Rus',
                                                    color=(255, 255, 255, 255),
                                                    font_size=10,
                                                    x=self.gl.WIDTH // 2, y=60)

    def draw(self):
        inventory = self.gl.gui.GUI_TEXTURES["inventory"]
        sel_inventory = self.gl.gui.GUI_TEXTURES["sel_inventory"]

        fullheart = self.gl.gui.GUI_TEXTURES["fullheart"]
        halfheart = self.gl.gui.GUI_TEXTURES["halfheart"]
        heartbg = self.gl.gui.GUI_TEXTURES["heartbg"]

        inventory.blit(self.gl.WIDTH // 2 - (inventory.width // 2), 0)
        sel_inventory.blit((self.gl.WIDTH // 2 - (inventory.width // 2)) +
                           (40 * self.activeInventory), 0)

        if self.gl.inventory_textures:
            for i in range(9):
                if self.inventory[i][1] == 0:
                    continue
                self.gl.inventory_textures[self.inventory[i][0]].blit(
                    (self.gl.WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 11, 11)
                self.blocksLabel[i].x = (self.gl.WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 22
                self.blocksLabel[i].y = 6
                self.blocksLabel[i].text = str(self.inventory[i][1])
                self.blocksLabel[i].draw()

        for i in range(10):
            ay = 0
            if self.gl.player.hp <= 3:
                ay = self.heartAnimation[i][0]
                if self.heartAnimation[i][1] == "-":
                    self.heartAnimation[i][0] -= 0.7
                else:
                    self.heartAnimation[i][0] += 0.7

                if self.heartAnimation[i][0] > 2:
                    self.heartAnimation[i][1] = "-"
                elif self.heartAnimation[i][0] < -2:
                    self.heartAnimation[i][1] = "+"

            heartbg.blit((self.gl.WIDTH // 2 - (inventory.width // 2)) + ((heartbg.width - 1) * i),
                         inventory.height + 10 + ay)

        cntr = 0
        ch = 0
        x = (self.gl.WIDTH // 2 - (inventory.width // 2)) + 2
        for i in range(self.gl.player.hp):
            ay = 0
            if self.gl.player.hp <= 3:
                ay = self.heartAnimation[ch][0]

            if cntr == 0:
                hrt = halfheart
                cntr = 1
            else:
                cntr = 0
                hrt = fullheart

            hrt.blit(x, inventory.height + 12 + ay)

            if hrt == fullheart:
                x += heartbg.width - 1
                ch += 1
