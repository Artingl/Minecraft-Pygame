from random import randint

from OpenGL.GL import *

from functions import roundPos


class droppedBlock:
    def __init__(self, gl):
        self.gl = gl
        self.blocks = {}

    def addBlock(self, coords, name):
        self.blocks[len(self.blocks)] = [coords, name, randint(0, 2) / 10]

    def update(self):
        cpy = self.blocks.copy().items()
        for i in cpy:

            pp = list(self.gl.player.position)
            sx, sy, sz = 0.25, 0.25, 0.25

            x, y, z = i[1][0][0] - i[1][2], i[1][0][1] + 0.1, i[1][0][2] + i[1][2]
            X, Y, Z = x + sx, y + sy, z + sz

            br = False
            for xs in (1, 0, -1):
                for ys in (1, 0, -1, -2):
                    for zs in (1, 0, -1):
                        if roundPos((pp[0] + xs, pp[1] + ys, pp[2] + zs)) == roundPos((x, y, z)):
                            self.blocks.pop(i[0])
                            self.gl.blockSound.playPickUpSound()
                            self.gl.player.inventory.addBlock(i[1][1])
                            br = True
                        if br:
                            break
                    if br:
                        break
                if br:
                    break
            if br:
                continue

            block = self.gl.block[i[1][1]]
            tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
            self.gl.stuffBatch.add(4, GL_QUADS, block[4], ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z)),
                                   tex_coords)  # back
            self.gl.stuffBatch.add(4, GL_QUADS, block[5], ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
                                   tex_coords)  # front

            self.gl.stuffBatch.add(4, GL_QUADS, block[0], ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
                                   tex_coords)  # left
            self.gl.stuffBatch.add(4, GL_QUADS, block[1], ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z)),
                                   tex_coords)  # right

            self.gl.stuffBatch.add(4, GL_QUADS, block[2], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)),
                                   tex_coords)  # bottom
            self.gl.stuffBatch.add(4, GL_QUADS, block[3], ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)),
                                   tex_coords)  # top

            yy = i[1][0][1]
            if roundPos((i[1][0][0], i[1][0][1], i[1][0][2])) not in self.gl.cubes.cubes:
                yy -= 0.1
            self.blocks[i[0]][0] = (i[1][0][0], yy, i[1][0][2])
