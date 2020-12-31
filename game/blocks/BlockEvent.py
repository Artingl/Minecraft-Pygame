from game.blocks.CraftingTable import CraftingTable
from game.world.Explosion import Explosion


def openBlockInventory(playerClass, blockClass, gl):
    if blockClass.name == "crafting_table":
        craftingtable = CraftingTable(playerClass, blockClass)

    if blockClass.name == "tnt":
        gl.blockSound.playBoomSound()
        exp = Explosion(gl, blockClass.p, 5, blockClass)
        exp.run()


def canOpenBlock(playerClass, blockClass, gl):
    if blockClass.name == "crafting_table":
        return True

    if blockClass.name == "tnt" and \
            playerClass.inventory.inventory[playerClass.inventory.activeInventory][0] == "log_oak":
        return True

    return False
