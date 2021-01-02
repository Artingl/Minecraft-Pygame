import os

from game.sound.BlockSound import BlockSound
from game.sound.Sound import Sound
from Gui import Gui
import pyglet
from game.entity.Player import Player
from openGL.Scene import Scene
from settings import *
from OpenGL.GL import *


def drawInfoLabel(text):
    y = 0
    for i in text.split("\n"):
        lbl = pyglet.text.Label(i,
                                font_name='Minecraft Rus',
                                color=(255, 255, 255, 255),
                                font_size=15,
                                x=0, y=WIDTH // 2 + y)
        lbl.set_style("background_color", (104, 104, 104, 160))
        lbl.draw()
        y -= 21


print("Loading the game...")

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Minecraft 1.0.0")

gui = Gui()
sound = Sound()
scene = Scene()
blockSound = BlockSound(scene)
player = Player(gl=scene)

player.position = [0, -90, 0]

scene.blockSound = blockSound
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

print("Loading step sounds...")
sound.BLOCKS_SOUND["step"] = {}
for e, i in enumerate(os.listdir("sounds/step/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.BLOCKS_SOUND["step"]:
        sound.BLOCKS_SOUND["step"][soundName] = []

    sound.BLOCKS_SOUND["step"][soundName].append(pygame.mixer.Sound("sounds/step/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading dig sounds...")
sound.BLOCKS_SOUND["dig"] = {}
for e, i in enumerate(os.listdir("sounds/dig/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.BLOCKS_SOUND["dig"]:
        sound.BLOCKS_SOUND["dig"][soundName] = []

    sound.BLOCKS_SOUND["dig"][soundName].append(pygame.mixer.Sound("sounds/dig/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading explode sounds...")
sound.BLOCKS_SOUND["explode"] = []
for e, i in enumerate(os.listdir("sounds/explode/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    sound.BLOCKS_SOUND["explode"].append(pygame.mixer.Sound("sounds/explode/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading damage sounds...")
sound.SOUNDS["damage"] = {}
for e, i in enumerate(os.listdir("sounds/damage/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.SOUNDS["damage"]:
        sound.SOUNDS["damage"][soundName] = []

    sound.SOUNDS["damage"][soundName].append(pygame.mixer.Sound("sounds/damage/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading music...")
for e, i in enumerate(os.listdir("sounds/music/")):
    sound.MUSIC.append("sounds/music/" + i)
sound.initMusic()
print("Music loaded successful!")

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
        drawInfoLabel(f"FPS: {round(clock.get_fps())}\n"
                      f"X Y Z: {round(player.x(), 3)}  {round(player.y(), 3)}  {round(player.z(), 3)}\n"
                      f"World seed: {scene.worldGen.seed}\n"
                      f"Count of particles: {len(scene.particles.particles)}\n"
                      f"Chunks: {scene.chunkg}")
    pygame.display.flip()
    clock.tick(MAX_FPS)
