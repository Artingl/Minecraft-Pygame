from game.Chunks import Chunks
from Gui import Gui
import pyglet
from game.Player import Player
from openGL.Scene import Scene
from settings import *
from OpenGL.GL import *

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Minecraft 1.0.0")

gui = Gui()
chunks = Chunks()
scene = Scene()
player = Player(gl=scene)

player.position = [0, 64, 0]

chunks.start()
scene.gui = gui
scene.player = player
scene.initScene()

gui.GUI_TEXTURES = {
        "crafting_table": pyglet.resource.image("gui/crafting_table.png"),
        "crosshair": pyglet.resource.image("gui/crosshair.png"),
        "inventory": pyglet.resource.image("gui/inventory.png"),
        "sel_inventory": pyglet.resource.image("gui/sel_inventory.png"),
}

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
texture = gui.GUI_TEXTURES["inventory"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["sel_inventory"]
texture.width *= 2
texture.height *= 2

gui.addGuiElement("crosshair", (WIDTH // 2 - 20, HEIGHT // 2 - 20))

showInfoLabel = False
infoLabel = pyglet.text.Label("",
                              font_name='Minecraft Rus',
                              color=(255, 255, 255, 255),
                              font_size=15,
                              x=0, y=WIDTH // 2 + 62)
infoLabel.set_style("background_color", (104, 104, 104, 160))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                PAUSE = not PAUSE
            if event.key == pygame.K_F3:
                showInfoLabel = not showInfoLabel
            if event.key == pygame.K_F5:
                player.cameraType += 1
                if player.cameraType > 3:
                    player.cameraType = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.mouseEvent(event.button)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                player.inventory.activeInventory -= 1
                gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
            elif event.button == 5:
                player.inventory.activeInventory += 1
                gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
    pygame.mouse.set_visible(PAUSE)
    if PAUSE:
        continue

    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
    scene.updateScene()

    player.inventory.draw()
    gui.update()

    if showInfoLabel:
        infoLabel.text = f"FPS: {round(clock.get_fps())}   " \
                         f"X Y Z: {round(player.x(), 3)}  {round(player.y(), 3)}  {round(player.z(), 3)}   " \
                         f"World seed: {scene.worldGen.seed}"
        infoLabel.draw()
    pygame.display.flip()
    clock.tick(MAX_FPS)
