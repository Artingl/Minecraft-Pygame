import math
from random import randint

import pyglet
from pyglet.gl import GL_QUADS

from game.GUI.ModalWindow import ModalWindow
from settings import *


class Inventory:
    def __init__(self, glClass):
        self.gl = glClass
        self.inventory = {}
        self.blocksLabel = {}
        self.activeInventory = 0
        self.heartAnimation = []
        self.draggingItem = []

        ls = list(self.gl.inventory_textures.items())
        old = False
        for i in range(10):
            old = not old
            self.heartAnimation.append([0, '-' if old else '+', randint(3, 8) / 10])
        for i in range(9 * 5 + 1):
            block = ls[1][0]

            self.inventory[i] = [block, 0]
            self.blocksLabel[i] = pyglet.text.Label("0",
                                                    font_name='Minecraft Rus',
                                                    color=(255, 255, 255, 255),
                                                    font_size=10,
                                                    x=self.gl.WIDTH // 2, y=60)

    def initWindow(self):
        self.window = ModalWindow(self.gl)
        self.window.setWindow(self.gl.gui.GUI_TEXTURES["inventory_window"])
        self.window.clickEvent = self.windowClickEvent
        self.window.updateFunctions.append(self.updateWindow)

        x = 16
        for i in range(9):
            self.window.cellPositions[i] = [(x, 284), None]
            x += 36

        x, y = 196, 36
        self.window.cellPositions[37] = [(x, y), None]
        x += 36
        self.window.cellPositions[38] = [(x, y), None]
        x = 196
        y += 36
        self.window.cellPositions[39] = [(x, y), None]
        x += 36
        self.window.cellPositions[40] = [(x, y), None]

        x, y = 16, 168
        for i in range(9 * 3, 0, -1):
            self.window.cellPositions[9 + i] = [(x, y), None]

            x += 36
            if x > 304:
                x = 16
                y += 36

    def showWindow(self):
        self.window.show()

    def windowClickEvent(self, button, cell):
        if button[0]:
            if self.draggingItem:
                if self.inventory[cell][1] == 0:
                    self.inventory[cell] = self.draggingItem
                    self.draggingItem = []
                else:
                    safe = [self.inventory[cell][0], self.inventory[cell][1]]
                    self.inventory[cell] = self.draggingItem
                    self.draggingItem = safe
            else:
                if self.inventory[cell][1] != 0:
                    self.draggingItem = [self.inventory[cell][0], self.inventory[cell][1]]
                    self.inventory[cell][1] = 0
        if button[2]:
            if self.draggingItem:
                if self.inventory[cell][0] == self.draggingItem[0] and self.draggingItem[1]:
                    self.inventory[cell][1] += 1
                    self.draggingItem[1] -= 1
                elif self.inventory[cell][1] == 0 and self.draggingItem[1]:
                    self.inventory[cell][0] = self.draggingItem[0]
                    self.inventory[cell][1] += 1
                    self.draggingItem[1] -= 1

    def updateWindow(self, win, mousePos):
        for i in self.window.cellPositions.items():
            xx, yy = self.window.cellPositions[i[0]][0][0], self.window.cellPositions[i[0]][0][1]

            self.window.cellPositions[i[0]][1] = self.inventory[i[0]]
            inv = self.inventory[i[0]]

            if inv[1] == 0 or inv[0] == 0:
                continue
            self.gl.inventory_textures[inv[0]].blit((self.gl.WIDTH // 2 - (win.width // 2)) + xx + 5,
                                                    (self.gl.HEIGHT // 2 + (win.height // 2)) - yy - 27)
            if inv[1] > 1:
                lx = (self.gl.WIDTH // 2 - (win.width // 2)) + xx + 15
                ly = (self.gl.HEIGHT // 2 + (win.height // 2)) - yy - 32
                lbl = pyglet.text.Label(str(inv[1]),
                                        font_name='Minecraft Rus',
                                        color=(255, 255, 255, 255),
                                        font_size=10,
                                        x=lx, y=ly)
                lbl.draw()

        if self.draggingItem:
            if self.draggingItem[1]:
                drg = self.draggingItem
                mp = list(mousePos)
                mp[0] -= 11
                mp[1] += 11

                self.gl.inventory_textures[drg[0]].blit(mp[0], self.gl.HEIGHT - mp[1])

                lx = mp[0] + 11
                ly = self.gl.HEIGHT - mp[1] - 5
                lbl = pyglet.text.Label(str(drg[1]),
                                        font_name='Minecraft Rus',
                                        color=(255, 255, 255, 255),
                                        font_size=10,
                                        x=lx, y=ly)
                lbl.draw()

    def addBlock(self, name):
        ext = False
        extech = -1
        sech = -1
        for item in self.inventory.items():
            i = item[1]
            if i[1] == 0 and sech == -1:
                sech = item[0]
            elif i[1] != 0:
                if i[0] == name and i[1] + 1 <= 64:
                    ext = True
                    extech = item[0]
                    break
        if ext:
            self.inventory[extech][1] += 1
        else:
            if self.inventory[self.activeInventory][1] == 0:
                sech = self.activeInventory
            self.inventory[sech] = [name, 1]

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
                if self.inventory[i][1] == 0 or self.inventory[i][0] == 0:
                    continue
                self.gl.inventory_textures[self.inventory[i][0]].blit(
                    (self.gl.WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 11, 11)
                self.blocksLabel[i].x = (self.gl.WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 22
                self.blocksLabel[i].y = 6
                self.blocksLabel[i].text = str(self.inventory[i][1])
                self.blocksLabel[i].draw()

        for i in range(10):
            ay = 0
            if self.gl.player.hp <= 6:
                ay = self.heartAnimation[i][0]
                if self.heartAnimation[i][1] == "-":
                    self.heartAnimation[i][0] -= self.heartAnimation[i][2]
                else:
                    self.heartAnimation[i][0] += self.heartAnimation[i][2]

                if self.heartAnimation[i][0] > 1:
                    self.heartAnimation[i][1] = "-"
                elif self.heartAnimation[i][0] < -1:
                    self.heartAnimation[i][1] = "+"

            heartbg.blit((self.gl.WIDTH // 2 - (inventory.width // 2)) + ((heartbg.width - 1) * i),
                         inventory.height + 10 + ay)

        cntr = 0
        ch = 0
        x = (self.gl.WIDTH // 2 - (inventory.width // 2)) + 2
        for i in range(self.gl.player.hp):
            ay = 0
            if self.gl.player.hp <= 6:
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
