import os
from random import randint

from functions import drawInfoLabel
from game.sound.BlockSound import BlockSound
from game.sound.Sound import Sound
from Gui import Gui
import pyglet
from game.entity.Player import Player
from openGL.Scene import Scene
from settings import *
from OpenGL.GL import *


def checkHover(ox, oy, ow, oh, mx, my):
    if ox < mx < ox + ow and oy < my < oy + oh:
        return True
    return False


def drawMainMenu(mc):
    global mainMenuRotation, IN_MENU, PAUSE
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.7, 1, 1))
    glFogf(GL_FOG_START, 60)
    glFogf(GL_FOG_END, 120)

    scene.set3d()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glRotatef(mainMenuRotation[0], 1, 0, 0)
    glRotatef(mainMenuRotation[1], 0, 1, 0)

    scene.draw()
    scene.drawPanorama()

    glPopMatrix()
    scene.set2d()
    mp = pygame.mouse.get_pos()

    drawInfoLabel("Minecraft 1.5.2", xx=10, yy=10, style=[('', '')], size=12)

    tex = gui.GUI_TEXTURES["game_logo"]
    tex.blit(WIDTH // 2 - (tex.width // 2), HEIGHT - tex.height - (HEIGHT // 15))

    # Singleplayer button
    but_tex = gui.GUI_TEXTURES["button_bg"]
    if checkHover(WIDTH // 2 - (but_tex.width // 2), HEIGHT // 2 - (but_tex.height // 2),
                  but_tex.width, but_tex.height,
                  mp[0], mp[1]):
        but_tex = gui.GUI_TEXTURES["button_bg_hover"]
        if mc == 1:
            menuChannelSound.stop()
            IN_MENU = False
            PAUSE = False

    but_tex.blit(WIDTH // 2 - (but_tex.width // 2), HEIGHT // 2 - (but_tex.height // 2))
    drawInfoLabel("Singleplayer", xx=WIDTH // 2, yy=HEIGHT // 2 - (but_tex.height // 2) + 14, style=[('', '')],
                  size=12, anchor_x='center')
    #

    # Quit button
    but_tex = gui.GUI_TEXTURES["button_bg"]
    if checkHover(WIDTH // 2 - (but_tex.width // 2), HEIGHT // 2 - (but_tex.height // 2) + 50,
                  but_tex.width, but_tex.height,
                  mp[0], mp[1]):
        but_tex = gui.GUI_TEXTURES["button_bg_hover"]
        if mc == 1:
            exit()

    but_tex.blit(WIDTH // 2 - (but_tex.width // 2), HEIGHT // 2 - (but_tex.height // 2) - 50)
    drawInfoLabel("Quit game", xx=WIDTH // 2, yy=HEIGHT // 2 - (but_tex.height // 2) + 14 - 50, style=[('', '')],
                  size=12, anchor_x='center')
    #

    pygame.display.flip()
    clock.tick(MAX_FPS)

    if mainMenuRotation[0] < 25:
        mainMenuRotation[2] = False
    if mainMenuRotation[0] > 75:
        mainMenuRotation[2] = True

    if mainMenuRotation[2]:
        mainMenuRotation[0] -= 0.008
    else:
        mainMenuRotation[0] += 0.008
    mainMenuRotation[1] += 0.02


print("Loading the game...")

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
pygame.display.set_caption("Minecraft 1.5.2")

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
    "game_logo": pyglet.resource.image("gui/game_logo.png"),
    "button_bg": pyglet.resource.image("gui/gui_elements/button_bg.png"),
    "button_bg_hover": pyglet.resource.image("gui/gui_elements/button_bg_hover.png"),
    "edit_bg": pyglet.resource.image("gui/gui_elements/edit_bg.png"),
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

texture = gui.GUI_TEXTURES["game_logo"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["button_bg"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["button_bg_hover"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["edit_bg"]
texture.width *= 2
texture.height *= 2

gui.addGuiElement("crosshair", (WIDTH // 2 - 9, HEIGHT // 2 - 9))

showInfoLabel = False

menuChannelSound = pygame.mixer.music
menuSound = ["sounds/music/10.mp3", "sounds/music/11.mp3", "sounds/music/12.mp3", "sounds/music/13.mp3"]
musicNum = randint(0, len(menuSound) - 1)
menuChannelSound.load(menuSound[musicNum])
for i in range(len(menuSound)):
    if i == musicNum:
        continue
    menuChannelSound.queue(menuSound[i])
menuChannelSound.play()
menuChannelSound.queue(menuSound[i])
menuChannelSound.set_volume(sound.volume)

print("Loading complete!")
mainMenuRotation = [50, 180, True]

while True:
    mbclicked = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mbclicked = event.button
        if not IN_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    PAUSE = not PAUSE
                if event.key == pygame.K_1:
                    player.inventory.activeInventory = 0
                if event.key == pygame.K_2:
                    player.inventory.activeInventory = 1
                if event.key == pygame.K_3:
                    player.inventory.activeInventory = 2
                if event.key == pygame.K_4:
                    player.inventory.activeInventory = 3
                if event.key == pygame.K_5:
                    player.inventory.activeInventory = 4
                if event.key == pygame.K_6:
                    player.inventory.activeInventory = 5
                if event.key == pygame.K_7:
                    player.inventory.activeInventory = 6
                if event.key == pygame.K_8:
                    player.inventory.activeInventory = 7
                if event.key == pygame.K_9:
                    player.inventory.activeInventory = 8
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

    if IN_MENU:
        drawMainMenu(mbclicked)

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
