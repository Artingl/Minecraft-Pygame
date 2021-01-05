import pygame
from OpenGL.GL import *
from functions import checkHover


class ModalWindow:
    def __init__(self, gl):
        self.gl = gl
        self.cellPositions = {}

        self.windowId = 0
        self.window = None

    def setWindow(self, win):
        self.window = win

    def destroyWindow(self):
        self.gl.allowEvents["keyboard"] = True
        self.gl.allowEvents["grabMouse"] = True
        self.gl.allowEvents["movePlayer"] = True
        self.gl.allowEvents["showCrosshair"] = True

        self.gl.updateEvents.pop(self.windowId)

    def drawWindow(self):
        self.gl.allowEvents["keyboard"] = False
        self.gl.allowEvents["grabMouse"] = False
        self.gl.allowEvents["movePlayer"] = False
        self.gl.allowEvents["showCrosshair"] = False

        win = self.window
        win.blit(self.gl.WIDTH // 2 - (win.width // 2), self.gl.HEIGHT // 2 - (win.height // 2))


        mp = pygame.mouse.get_pos()

        hover = self.gl.gui.GUI_TEXTURES["selected"]
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        for i in self.cellPositions.items():
            w, h = 32, 32
            if len(i[1][0]) > 2:
                w, h = i[1][0][2], i[1][0][3]
            x, y, block = i[1][0][0], i[1][0][1], i[1][1]
            x += self.gl.WIDTH // 2 - (win.width // 2)
            y += self.gl.HEIGHT // 2 - (win.height // 2)
            if checkHover(x, y, w, h, mp[0], mp[1]):
                print(i[0])
                hover.width = w
                hover.height = h
                hover.blit(x, self.gl.HEIGHT - y - h)

        by = 117
        for i in self.cellPositions.items():
            if i[0] <= 9:
                continue
            bid = 45 - i[0]
            xx, yy = self.cellPositions[bid + 10][0][0], self.cellPositions[bid + 10][0][1]

            self.cellPositions[bid + 9][1] = self.gl.player.inventory.inventory[bid]
            inv = self.gl.player.inventory.inventory[bid]

            if inv[1] == 0:
                continue
            self.gl.inventory_textures[inv[0]].blit((self.gl.WIDTH // 2 - (win.width // 2)) + xx + 5,
                                                    (self.gl.HEIGHT // 2 + (win.height // 2)) - yy + by - 27)
            if by == 117 and bid % 9 == 0:
                by -= 9
            if bid % 9 == 0:
                by -= 72
            if by == -108:
                by -= 9

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.destroyWindow()
            return

    def show(self):
        self.gl.updateEvents.append(self.drawWindow)
        self.windowId = len(self.gl.updateEvents) - 1
