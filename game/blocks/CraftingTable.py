from game.GUI.ModalWindow import ModalWindow
from settings import *


class CraftingTable:
    def __init__(self, plClass, blClass):
        # TODO: do crafting table

        self.pc = plClass
        self.bc = blClass
        self.gl = self.pc.gl

        self.window = ModalWindow(self.gl)
        self.window.setWindow(self.gl.gui.GUI_TEXTURES["crafting_table"])

        self.window.cellPositions = {0: [(60, 34), None], 1: [(96, 34), None], 2: [(132, 34), None],
                                     3: [(60, 70), None], 4: [(96, 70), None], 5: [(132, 70), None],
                                     6: [(60, 106), None], 7: [(96, 106), None], 8: [(132, 106), None],
                                     9: [(240, 62, 48, 48), None]}

        x, y = 16, 168
        for i in range(9 * 3 + 1):
            self.window.cellPositions[i + 10] = [(x, y), None]

            x += 36
            if x > 304:
                x = 16
                y += 36

        x = 16
        for i in range(9):
            self.window.cellPositions[i + 37] = [(x, 284), None]
            x += 36

        self.window.updateFunctions.append(self.update)
        self.window.show()

    def update(self, win, mousePos):
        by = 117
        for i in self.window.cellPositions.items():
            if i[0] <= 9:
                continue
            bid = 45 - i[0]
            xx, yy = self.window.cellPositions[bid + 10][0][0], self.window.cellPositions[bid + 10][0][1]

            self.window.cellPositions[bid + 9][1] = self.gl.player.inventory.inventory[bid]
            inv = self.gl.player.inventory.inventory[bid]

            if inv[1] == 0 or inv[0] == 0:
                continue
            self.gl.inventory_textures[inv[0]].blit((self.gl.WIDTH // 2 - (win.width // 2)) + xx + 5,
                                                    (self.gl.HEIGHT // 2 + (win.height // 2)) - yy + by - 27)
            if by == 117 and bid % 9 == 0:
                by -= 9
            if bid % 9 == 0:
                by -= 72
            if by == -108:
                by -= 9
