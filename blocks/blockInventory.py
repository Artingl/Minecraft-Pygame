from blocks.CraftingTable import CraftingTable
from settings import *


def openBlockInventory(playerClass, blockClass):
    if blockClass.name == "crafting_table":
        craftingtable = CraftingTable(playerClass, blockClass)


def canOpenBlock(blockClass):
    if blockClass.name == "crafting_table":
        return True

    return False
