from settings import *


class CraftingTable:
    def __init__(self, plClass, blClass):
        self.pc = plClass
        self.bc = blClass

        # self.pc.gl.gui.addGuiElement("crafting_table", (WIDTH // 2, HEIGHT // 2))
        # self.waitForExit()

    def waitForExit(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            return
