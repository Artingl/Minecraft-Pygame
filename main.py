import os
import time

from Sound import Sound
from Gui import Gui
import pyglet
from game.entity.Player import Player
from openGL.Scene import Scene
from settings import *
from OpenGL.GL import *

print("Loading the game...")

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Minecraft 1.0.0")

gui = Gui()
sound = Sound()
scene = Scene()
player = Player(gl=scene)

player.position = [0, -90, 0]

scene.gui = gui
scene.sound = sound
scene.player = player
scene.initScene()

# Loading screen
glClearColor(1, 1, 1, 1)

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()

scene.set2d()
logo = pyglet.resource.image("gui/logo.png")
logo.blit(WIDTH // 2 - (logo.width // 2), HEIGHT // 2 - (logo.height // 2))
pygame.display.flip()
#

print("Loading sounds...")
sound.SOUNDS = {
    "oof": pygame.mixer.Sound("sounds/oof.mp3"),
}

print("Loading music...")
for e, i in enumerate(os.listdir("sounds/music/")):
    sound.MUSIC.append(pygame.mixer.Sound("sounds/music/" + i))
    print("Successful loaded", i, "music!")

print("Loading GUI textures...")
gui.GUI_TEXTURES = {
        "crafting_table": pyglet.resource.image("gui/crafting_table.png"),
        "crosshair": pyglet.resource.image("gui/crosshair.png"),
        "inventory": pyglet.resource.image("gui/inventory.png"),
        "sel_inventory": pyglet.resource.image("gui/sel_inventory.png"),
        "fullheart": pyglet.resource.image("gui/fullheart.png"),
        "halfheart": pyglet.resource.image("gui/halfheart.png"),
        "heartbg": pyglet.resource.image("gui/heartbg.png"),
}

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
texture = gui.GUI_TEXTURES["inventory"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["sel_inventory"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["fullheart"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["halfheart"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["heartbg"]
texture.width *= 2
texture.height *= 2

gui.addGuiElement("crosshair", (WIDTH // 2 - 9, HEIGHT // 2 - 9))

showInfoLabel = False
infoLabel = pyglet.text.Label("",
                              font_name='Minecraft Rus',
                              color=(255, 255, 255, 255),
                              font_size=15,
                              x=0, y=WIDTH // 2 + 62)
infoLabel.set_style("background_color", (104, 104, 104, 160))
print("Loading complete!")

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
                if player.inventory.activeInventory < 0:
                    player.inventory.activeInventory = 8
                gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
            elif event.button == 5:
                player.inventory.activeInventory += 1
                if player.inventory.activeInventory > 8:
                    player.inventory.activeInventory = 0
                gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
    pygame.mouse.set_visible(PAUSE)
    if PAUSE:
        continue
    sound.playMusic()

    pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
    scene.updateScene()

    player.inventory.draw()
    gui.update()

    if showInfoLabel:
        infoLabel.text = f"FPS: {round(clock.get_fps())}   " \
                         f"X Y Z: {round(player.x(), 3)}  {round(player.y(), 3)}  {round(player.z(), 3)}   " \
                         f"World seed: {scene.worldGen.seed}   " \
                         f"Count of particles: {len(scene.particles.particles)}   " \
                         f"Chunks: {scene.chunkg}"
        infoLabel.draw()
    pygame.display.flip()
    clock.tick(MAX_FPS)
