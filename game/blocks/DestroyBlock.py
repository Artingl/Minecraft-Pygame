import os

import pyglet
from OpenGL.GL import *


class DestroyBlock:
    def __init__(self, gl):
        self.gl = gl
        self.destroyStage = -1
        self.textures = {}

        self.loadTextures()

    def loadTextures(self):
        print("Loading block destroy textures...")
        for e, i in enumerate(os.listdir("textures/blocks/block_destroy")):
            self.textures[e] = \
                pyglet.graphics.TextureGroup(pyglet.image.load("textures/blocks/block_destroy/" + i)
                                             .get_mipmapped_texture())
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def drawDestroy(self, x, y, z):
        if self.destroyStage == -1:
            return

        s = 1.01
        x += s / 2
        y += s / 2
        z += s / 2
        X, Y, Z = x - s, y - s, z - s

        vertexes = [
            (X, y, z, x, y, z, x, Y, z, X, Y, z),
            (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z),
            (x, y, z, x, y, Z, x, Y, Z, x, Y, z),
            (X, y, Z, X, y, z, X, Y, z, X, Y, Z),
            (x, y, z, X, y, z, X, y, Z, x, y, Z),
            (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z),
        ]

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        mode = GL_QUADS
        stg = int(self.destroyStage)
        self.gl.stuffBatch.add(4, mode, self.textures[stg], ('v3f', vertexes[0]),
                               tex_coords)  # back
        self.gl.stuffBatch.add(4, mode, self.textures[stg], ('v3f', vertexes[1]),
                               tex_coords)  # front

        self.gl.stuffBatch.add(4, mode, self.textures[stg], ('v3f', vertexes[2]),
                               tex_coords)  # left
        self.gl.stuffBatch.add(4, mode, self.textures[stg], ('v3f', vertexes[3]),
                               tex_coords)  # right

        self.gl.stuffBatch.add(4, mode, self.textures[stg], ('v3f', vertexes[4]),
                               tex_coords)  # bottom

        self.gl.stuffBatch.add(4, mode, self.textures[stg], ('v3f', vertexes[5]),
                               tex_coords)  # top

    def destroy(self, blockName, blockByVec):
        if self.destroyStage == -1:
            self.destroyStage = 0
        self.destroyStage += 0.1
        if self.destroyStage > 9:
            self.destroyStage = -1
            if blockByVec[0] in self.gl.cubes.cubes:
                if self.gl.player.inventory.inventory[self.gl.player.inventory.activeInventory][0] == \
                        self.gl.cubes.cubes[blockByVec[0]].name:
                    self.gl.player.inventory.inventory[self.gl.player.inventory.activeInventory][1] += 1
                elif self.gl.player.inventory.inventory[self.gl.player.inventory.activeInventory][1] == 0:
                    self.gl.player.inventory.inventory[self.gl.player.inventory.activeInventory][1] += 1
                    self.gl.player.inventory.inventory[self.gl.player.inventory.activeInventory][0] = \
                        self.gl.cubes.cubes[blockByVec[0]].name
            self.gl.blockSound.playBlockSound(self.gl.cubes.cubes[blockByVec[0]].name)
            self.gl.particles.addParticle(self.gl.cubes.cubes[blockByVec[0]].p, self.gl.cubes.cubes[blockByVec[0]],
                                          direction="down")
            self.gl.cubes.remove(blockByVec[0])
