import math
import os
from random import randint
import pyglet
from OpenGL.GL import *
from functions import drawInfoLabel, getElpsTime
from game.GUI.Button import Button
from game.GUI.GUI import GUI
from game.entity.Player import Player
from game.sound.BlockSound import BlockSound
from game.sound.Sound import Sound
from openGL.Scene import Scene
from settings import *


def quitToMenu():
    global PAUSE, IN_MENU, mainFunction

    tex = gui.GUI_TEXTURES["options_background"]
    tex2 = gui.GUI_TEXTURES["black"]
    for x in range(0, scene.WIDTH, tex.width):
        for y in range(0, scene.HEIGHT, tex.height):
            tex.blit(x, y)
            tex2.blit(x, y)
    drawInfoLabel(scene, "Quitting to main menu", xx=scene.WIDTH // 2, yy=scene.HEIGHT // 2,
                  style=[('', '')], size=12, anchor_x='center')
    pygame.display.flip()
    clock.tick(MAX_FPS)

    PAUSE = True
    IN_MENU = True

    sound.initMusic(False)

    sound.musicPlayer.play()
    sound.musicPlayer.set_volume(sound.volume)

    scene.resetScene()
    scene.initScene()

    player.position = [0, -90, 0]
    mainFunction = drawMainMenu


def showSettings():
    global mainFunction
    mainFunction = genWorld


def startNewGame():
    global mainFunction
    sound.musicPlayer.stop()
    sound.initMusic(True)
    mainFunction = genWorld


def pause():
    global PAUSE
    PAUSE = not PAUSE
    scene.allowEvents["movePlayer"] = True
    scene.allowEvents["keyboardAndMouse"] = True


def pauseMenu(mc):
    bg = gui.GUI_TEXTURES["black"]
    bg.width = scene.WIDTH
    bg.height = scene.HEIGHT
    bg.blit(0, 0)

    mp = pygame.mouse.get_pos()

    drawInfoLabel(scene, f"Game menu", xx=scene.WIDTH // 2, yy=scene.HEIGHT - scene.HEIGHT // 4, style=[('', '')],
                  size=12, anchor_x='center')

    # Back to Game button
    resumeButton.x = scene.WIDTH // 2 - (resumeButton.button.width // 2)
    resumeButton.y = scene.HEIGHT // 2 - (resumeButton.button.height // 2) - 50
    resumeButton.update(mp, mc)
    #

    # Quit to main menu button
    quitWorldButton.x = scene.WIDTH // 2 - (quitButton.button.width // 2)
    quitWorldButton.y = scene.HEIGHT // 2 - (quitButton.button.height // 2)
    quitWorldButton.update(mp, mc)
    #

    pygame.display.flip()
    clock.tick(MAX_FPS)


def genWorld(mc):
    global IN_MENU, PAUSE, resizeEvent

    scene.set2d()
    tex = gui.GUI_TEXTURES["options_background"]
    tex2 = gui.GUI_TEXTURES["black"]
    if scene.chunkg == len(scene.worldSp) or resizeEvent:
        for x in range(0, scene.WIDTH, tex.width):
            for y in range(0, scene.HEIGHT, tex.height):
                tex.blit(x, y)
                tex2.blit(x, y)
        resizeEvent = False
    else:
        for x in range(-2, 2):
            for y in range(-2, 2):
                ix, iy = (scene.WIDTH // 2) + (x * tex.width), (scene.HEIGHT // 2) + (y * tex.height)

                tex.blit(ix, iy)
                tex2.blit(ix, iy)

    scene.genWorld()
    if len(scene.worldSp) - scene.chunkg > 1:#220:
        IN_MENU = False
        PAUSE = False

    proc = round((len(scene.worldSp) - scene.chunkg) * 100 / 1)#220)
    drawInfoLabel(scene, "Loading world...", xx=scene.WIDTH // 2, yy=scene.HEIGHT // 2, style=[('', '')],
                  size=12, anchor_x='center')
    drawInfoLabel(scene, f"Generating terrain {proc}%...", xx=scene.WIDTH // 2, yy=scene.HEIGHT // 2 - 39,
                  style=[('', '')], size=12, anchor_x='center')

    pygame.display.flip()
    clock.tick(MAX_FPS)


def drawMainMenu(mc):
    global mainMenuRotation, IN_MENU, PAUSE
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.7, 1, 1))
    glFogf(GL_FOG_START, 0)
    glFogf(GL_FOG_END, 1000)

    scene.set3d()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glRotatef(mainMenuRotation[0], 1, 0, 0)
    glRotatef(mainMenuRotation[1], 0, 1, 0)
    glTranslatef(0, 0, 0)

    scene.draw()
    scene.drawPanorama()

    glPopMatrix()
    scene.set2d()
    mp = pygame.mouse.get_pos()

    tex = gui.GUI_TEXTURES["game_logo"]
    tex.blit(scene.WIDTH // 2 - (tex.width // 2), scene.HEIGHT - tex.height - (scene.HEIGHT // 15))

    drawInfoLabel(scene, f"Minecraft {MC_VERSION}", xx=10, yy=10, style=[('', '')], size=12)

    # Singleplayer button
    singleplayerButton.x = scene.WIDTH // 2 - (singleplayerButton.button.width // 2)
    singleplayerButton.y = scene.HEIGHT // 2 - (singleplayerButton.button.height // 2) - 25
    singleplayerButton.update(mp, mc)
    #

    # Options button
    optionsButton.x = scene.WIDTH // 2 - (optionsButton.button.width // 2)
    optionsButton.y = scene.HEIGHT // 2 - (optionsButton.button.height // 2) + 25
    optionsButton.update(mp, mc)
    #

    # Quit button
    quitButton.x = scene.WIDTH // 2 - (quitButton.button.width // 2)
    quitButton.y = scene.HEIGHT // 2 - (quitButton.button.height // 2) + 75
    quitButton.update(mp, mc)
    #

    # Splash
    glPushMatrix()
    glTranslatef((scene.WIDTH // 2 + (tex.width // 2)) - 90, scene.HEIGHT - tex.height - (scene.HEIGHT // 15) + 15, 0.0)
    glRotatef(20.0, 0.0, 0.0, 1.0)
    var8 = 1.8 - abs(math.sin((getElpsTime() % 1000) / 1000.0 * math.pi * 2.0) * 0.1)
    var8 = var8 * 100.0 / ((24 * 12) + 32)
    drawInfoLabel(scene, splash, xx=1, yy=1, style=[('', '')], scale=var8, size=30, anchor_x='center',
                  label_color=(255, 255, 0), shadow_color=(63, 63, 0))
    glPopMatrix()
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

resizeEvent = False
LAST_SAVED_RESOLUTION = [WIDTH, HEIGHT]

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
pygame.display.set_caption(f"Minecraft {MC_VERSION}")

sound = Sound()
scene = Scene()
gui = GUI(scene)
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
logo.blit(scene.WIDTH // 2 - (logo.width // 2), scene.HEIGHT // 2 - (logo.height // 2))
pygame.display.flip()
#

print("Loading sounds...")
sound.BLOCKS_SOUND["pickUp"] = pygame.mixer.Sound("sounds/pick.mp3")

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

print("Loading GUI sounds...")
sound.SOUNDS["GUI"] = {}
for e, i in enumerate(os.listdir("sounds/gui/")):
    soundName = i.split(".")[0][:-1]
    soundNum = i.split(".")[0][-1]

    if soundName not in sound.SOUNDS["GUI"]:
        sound.SOUNDS["GUI"][soundName] = []

    sound.SOUNDS["GUI"][soundName].append(pygame.mixer.Sound("sounds/gui/" + i))
    print("Successful loaded", soundName, "#" + soundNum, "sound!")

print("Loading menu music...")
for e, i in enumerate(os.listdir("sounds/music/menu")):
    sound.MENU_MUSIC.append("sounds/music/menu/" + i)
    print("Successful loaded", i, "music!")

print("Loading game music...")
for e, i in enumerate(os.listdir("sounds/music/game")):
    sound.MUSIC.append("sounds/music/game/" + i)
    print("Successful loaded", i, "music!")
sound.initMusic(False)

print("Music loaded successful!")

print("Loading GUI textures...")
gui.GUI_TEXTURES = {
    "crafting_table": pyglet.resource.image("gui/crafting_table.png"),
    "inventory_window": pyglet.resource.image("gui/inventory_window.png"),
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
    "options_background": pyglet.resource.image("gui/gui_elements/options_background.png"),
    "black": pyglet.resource.image("gui/gui_elements/black.png"),
    "selected": pyglet.resource.image("gui/gui_elements/selected.png"),
}

glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

texture = gui.GUI_TEXTURES["crafting_table"]
texture.width *= 2
texture.height *= 2

texture = gui.GUI_TEXTURES["inventory_window"]
texture.width *= 2
texture.height *= 2

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

texture = gui.GUI_TEXTURES["options_background"]
texture.width *= 6
texture.height *= 6

texture = gui.GUI_TEXTURES["black"]
texture.width *= 6
texture.height *= 6

texture = gui.GUI_TEXTURES["selected"]
texture.width *= 2
texture.height *= 2

gui.addGuiElement("crosshair", (scene.WIDTH // 2 - 9, scene.HEIGHT // 2 - 9))

player.inventory.initWindow()

showInfoLabel = False

print("Loading splashes...")
splfile = open("gui/splashes.txt", "r")
splash = splfile.read().split("\n")
splash = splash[randint(0, len(splash) - 1)]
splfile.close()

sound.musicPlayer.play()
sound.musicPlayer.set_volume(sound.volume)

# Main menu buttons
singleplayerButton = Button(scene, "Singleplayer", 0, 0)
optionsButton = Button(scene, "Options", 0, 0)
quitButton = Button(scene, "Quit game", 0, 0)

singleplayerButton.setEvent(startNewGame)
optionsButton.setEvent(showSettings)
quitButton.setEvent(exit)
#

# Pause menu buttons
resumeButton = Button(scene, "Back to Game", 0, 0)
quitWorldButton = Button(scene, "Quit to main menu", 0, 0)

resumeButton.setEvent(pause)
quitWorldButton.setEvent(quitToMenu)
#

print("Loading complete!")
mainMenuRotation = [50, 180, True]

mainFunction = drawMainMenu

while True:
    if scene.allowEvents["keyboardAndMouse"] and not PAUSE:
        if pygame.mouse.get_pressed(3)[0]:
            player.mouseEvent(1)
    mbclicked = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                if scene.WIDTH != monitor.current_w or scene.HEIGHT != monitor.current_h:
                    LAST_SAVED_RESOLUTION = [scene.WIDTH, scene.HEIGHT]

                    WIDTH = monitor.current_w
                    HEIGHT = monitor.current_h
                    screen = pygame.display.set_mode((monitor.current_w, monitor.current_h),
                                                     pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
                                                     | pygame.FULLSCREEN)
                    scene.resizeCGL(WIDTH, HEIGHT)
                    resizeEvent = True
                else:
                    WIDTH = LAST_SAVED_RESOLUTION[0]
                    HEIGHT = LAST_SAVED_RESOLUTION[1]
                    screen = pygame.display.set_mode((WIDTH, HEIGHT),
                                                     pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
                    scene.resizeCGL(WIDTH, HEIGHT)
                    resizeEvent = True
        if event.type == pygame.VIDEORESIZE:
            WIDTH = event.w
            HEIGHT = event.h
            scene.resizeCGL(WIDTH, HEIGHT)
            resizeEvent = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            mbclicked = event.button
        if not IN_MENU:
            if scene.allowEvents["keyboardAndMouse"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause()
                    if event.key == pygame.K_e:
                        player.inventory.showWindow()
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
                    if event.button == 4:
                        player.inventory.activeInventory -= 1
                        if player.inventory.activeInventory < 0:
                            player.inventory.activeInventory = 8
                        if player.inventory.inventory[player.inventory.activeInventory][1]:
                            gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
                    elif event.button == 5:
                        player.inventory.activeInventory += 1
                        if player.inventory.activeInventory > 8:
                            player.inventory.activeInventory = 0
                        if player.inventory.inventory[player.inventory.activeInventory][1]:
                            gui.showText(player.inventory.inventory[player.inventory.activeInventory][0])
                else:
                    if pygame.mouse.get_pressed(3)[0]:
                        player.mouseEvent(1)
                    else:
                        player.mouseEvent(-1)
    if scene.allowEvents["grabMouse"]:
        pygame.mouse.set_visible(PAUSE)
    else:
        pygame.mouse.set_visible(True)

    if IN_MENU:
        mainFunction(mbclicked)

    if not PAUSE:
        sound.playMusic()

        if scene.allowEvents["showCrosshair"]:
            gui.shows["crosshair"][1] = (scene.WIDTH // 2 - 9, scene.HEIGHT // 2 - 9)
        else:
            gui.shows["crosshair"][1] = (-100, -100)
        if scene.allowEvents["grabMouse"] and pygame.mouse.get_focused():
            pygame.mouse.set_pos((scene.WIDTH // 2, scene.HEIGHT // 2))
        scene.updateScene()

        player.inventory.draw()
        gui.update()

        if showInfoLabel:
            drawInfoLabel(scene, f"FPS: {round(clock.get_fps())}\n"
                          f"X Y Z: {round(player.x(), 3)}  {round(player.y(), 3)}  {round(player.z(), 3)}\n"
                          f"World seed: {scene.worldGen.seed}\n"
                          f"Count of particles: {len(scene.particles.particles)}\n"
                          f"Chunks: {scene.chunkg}")
        pygame.display.flip()
        clock.tick(MAX_FPS)
    elif PAUSE and not IN_MENU:
        scene.allowEvents["movePlayer"] = False
        scene.allowEvents["keyboardAndMouse"] = False
        if scene.allowEvents["showCrosshair"]:
            gui.shows["crosshair"][1] = (scene.WIDTH // 2 - 9, scene.HEIGHT // 2 - 9)
        else:
            gui.shows["crosshair"][1] = (-100, -100)
        scene.updateScene()

        player.inventory.draw()
        gui.update()

        pauseMenu(mbclicked)
