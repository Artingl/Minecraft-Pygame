import threading

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pyglet import shapes
from pyglet.gl import *

from blocks.Inventory import Inventory
from game.worldGenerator import worldGenerator
from openGL.CubeHandler import CubeHandler
from settings import *
from functions import *


class Scene:
    def __init__(self):
        self.worldSp = spiral(CHUNKS_RENDER_DISTANCE)
        self.chunkg = len(self.worldSp)
        self.drawCounter = 0
        self.in_water = False
        self.worldGen = worldGenerator(self, randint(434, 434343454))
        self.gui = None
        self.player = None
        self.texture, self.block, self.texture_dir, self.inventory_textures = {}, {}, {}, {}
        self.fov = FOV

    def vertexList(self):
        x, y, w, h = WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT
        self.reticle = pyglet.graphics.vertex_list(4, ('v2f', (x - 10, y, x + 10, y, x, y - 10, x, y + 10)),
                                                   ('c3f', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))

    def initScene(self):
        glClearColor(0.5, 0.7, 1, 1)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glAlphaFunc(GL_GEQUAL, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_FOG)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glEnable(GL_TEXTURE_2D)

        glLoadIdentity()
        load_textures(self)
        self.vertexList()

        self.transparent = pyglet.graphics.Batch()
        self.opaque = pyglet.graphics.Batch()
        self.player.inventory = Inventory(self)
        self.cubes = CubeHandler(self.opaque, self.block, self.opaque,
                                 ('leaves_taiga', 'leaves_oak', 'tall_grass', 'nocolor'), self)

        self.set3d()

    def set2d(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, WIDTH, 0, HEIGHT)

    def set3d(self):
        glLoadIdentity()
        gluPerspective(self.fov, (WIDTH / HEIGHT), 0.1, RENDER_DISTANCE * 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def updateScene(self):
        self.drawCounter += 1
        if self.drawCounter > 1 and self.chunkg > 0:
            self.drawCounter = 0
            x, y = self.worldSp[self.chunkg]
            self.chunkg -= 1
            self.worldGen.genChunk(CHUNKS_RENDER_DISTANCE // 2 - x, CHUNKS_RENDER_DISTANCE // 2 - y, self.player)
        if self.in_water:
            glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0, 0, 0, 1))
            glFogf(GL_FOG_START, 10)
            glFogf(GL_FOG_END, 35)
        else:
            glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.7, 1, 1))
            glFogf(GL_FOG_START, 60)
            glFogf(GL_FOG_END, 120)

        self.set3d()

        glClearColor(0.5, 0.7, 1, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.player.update()
        self.draw()

        blockByVec = self.cubes.hitTest(self.player.position, self.player.get_sight_vector())
        if blockByVec[0]:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3d(0, 0, 0)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', flatten(cube_vertices(blockByVec[0], 0.51))))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glColor3d(1, 1, 1)

        glPopMatrix()
        self.set2d()

        glBegin(GL_LINES)
        glVertex2f(-10, 0)
        glVertex2f(10, 1)
        glEnd()

    def draw(self):
        glEnable(GL_ALPHA_TEST)
        self.opaque.draw()
        glDisable(GL_ALPHA_TEST)
        glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
        self.transparent.draw()
        glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
        self.transparent.draw()
