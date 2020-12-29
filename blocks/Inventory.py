from settings import *


class Inventory:
    def __init__(self, glClass):
        self.gl = glClass
        self.inventory = {}
        self.activeInventory = 0
        for i in range(9):
            self.inventory[i] = ["stone", 64]

    def draw(self):
        if self.activeInventory > 8:
            self.activeInventory = 0
        if self.activeInventory < 0:
            self.activeInventory = 8

        inventory = self.gl.gui.GUI_TEXTURES["inventory"]
        sel_inventory = self.gl.gui.GUI_TEXTURES["sel_inventory"]

        inventory.blit(WIDTH // 2 - (inventory.width // 2), 0)
        sel_inventory.blit((WIDTH // 2 - (inventory.width // 2)) +
                           (40 * self.activeInventory), 0)

        if self.gl.inventory_textures:
            for i in range(9):
                self.gl.inventory_textures[self.inventory[i][0]].blit(
                    (WIDTH // 2 - (inventory.width // 2)) + (40 * i) + 11, 11)
