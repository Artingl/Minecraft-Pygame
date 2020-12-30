from random import randint

import pyglet

from settings import *


class Inventory:
    def __init__(self, glClass):
        self.gl = glClass
        self.inventory = {}
        self.blocksLabel = {}
        self.activeInventory = 0
        ls = list(self.gl.inventory_textures.items())
        for i in range(9):
            block = ls[i][0]
            if i == 0:
                block = "tnt"

            self.inventory[i] = [block, 64]
            self.blocksLabel[i] = pyglet.text.Label("0",
                                                    font_name='Minecraft Rus',
                                                    color=(255, 255, 255, 255),
                                                    font_size=10,
                                                    x=WIDTH // 2, y=60)

    def draw(self):
        inventory = self.gl.gui.GUI_TEXTURES["inventory"]
        sel_inventory = self.gl.gui.GUI_TEXTURES["sel_inventory"]

        inventory.blit(WIDTH // 2 - (inventory.width // 2), 0)
        sel_inventory.blit((WIDTH // 2 - (inventory.width // 2)) +
                           (40 * self.activeInventory), 0)

        if self.gl.inventory_textures:
            for i in range(9):
                if self.inventory[i][1] == 0:
                    continue
                self.gl.inventory_textures[self.inventory[i][0]].blit(
                    (WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 11, 11)
                self.blocksLabel[i].x = (WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 22
                self.blocksLabel[i].y = 6
                self.blocksLabel[i].text = str(self.inventory[i][1])
                self.blocksLabel[i].draw()
