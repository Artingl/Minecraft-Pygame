from blocks.CraftingTable import CraftingTable
from game.Explosion import Explosion
from settings import *


def openBlockInventory(playerClass, blockClass, gl):
    if blockClass.name == "crafting_table":
        craftingtable = CraftingTable(playerClass, blockClass)

    if blockClass.name == "tnt":
        exp = Explosion(gl, blockClass.p, 5, blockClass)
        exp.run()


def canOpenBlock(playerClass, blockClass, gl):
    if blockClass.name == "crafting_table":
        return True

    if blockClass.name == "tnt" and \
            playerClass.inventory.inventory[playerClass.inventory.activeInventory][0] == "log_oak":
        return True

    return False
